"""
ephaptic_spiking_field.py
=========================
The two sides of the standing wave, in ONE engine.

A continuous held FIELD s (the standing wave / the "content", the qualia-candidate)
is written by SPARSE SPIKES from integrate-and-fire spectral islands. Each island
holds a tuned pattern p_k (its Koopman mode / AIS grating); it reads its resonance
<p_k, s> with the shared field, integrates that drive plus Johnson-Nyquist thermal
noise, is gated by an 8 Hz theta excitability clock, suppressed by spike-frequency
adaptation, and when it crosses threshold it SPIKES and injects p_k back into the
field. The islands never touch each other directly -- only through the shared field.
That is ephaptic coupling; W = sum p_k p_k^T is the holographic plate.

  side A (content / qualia-candidate):  the continuous field s, held, mostly silent.
  side B (communication / EEG-visible):  the sparse, theta-locked spikes that update it.

TWO DEMONSTRATIONS, SAME ENGINE:

  DEMO 1 (distinct patterns):  Does the field hold a percept SILENTLY and update it
      with SPARSE, THETA-LOCKED spikes? (the delta-code the pure dreaming field could
      not produce -- it needed the clock.)

  DEMO 2 (direction-tiling islands):  Holding the non-circular standard of the CAN
      resonator -- input only a constant heading bias, the theta clock, the pattern
      overlaps (coupling) and adaptation; NEVER a sweep direction, length, or parity
      -- do hippocampal theta SWEEPS and left-right ALTERNATION EMERGE, switched on
      and off by the single adaptation parameter beta?

Do not hype. Do not lie. Just show.
PerceptionLab / Antti Luode, with Claude (Opus 4.8). Helsinki, June 2026.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec


# ============================================================
# The unified engine
# ============================================================
class EphapticSpikingField:
    """Continuous held field written by JN-noise integrate-and-fire spectral islands,
    paced by a theta clock, suppressed by adaptation. One step() = one dt."""

    def __init__(self, P, *, dt=0.001, f_theta=8.0, m_theta=0.8,
                 leak_v=0.90, thr=0.55, inject=0.18, field_leak=0.985,
                 sigma_JN=0.06, beta=2.0, tau_a=0.18, J_inh=0.0, bias=None, seed=1):
        self.P = P                       # (K, N) island patterns (unit norm)
        self.K, self.N = P.shape
        self.dt, self.f_theta, self.m_theta = dt, f_theta, m_theta
        self.leak_v, self.thr, self.inject = leak_v, thr, inject
        self.field_leak, self.sigma_JN = field_leak, sigma_JN
        self.beta, self.tau_a, self.J_inh = beta, tau_a, J_inh
        self.bias = np.zeros(self.K) if bias is None else bias
        self.rng = np.random.default_rng(seed)
        self.t = 0
        self.v = np.zeros(self.K)        # island membrane potentials
        self.a = np.zeros(self.K)        # spike-frequency adaptation
        self.s = None                    # the held field (set by seed_field)

    def seed_field(self, s0):
        self.s = s0 / (np.linalg.norm(s0) + 1e-9)

    def step(self):
        g = 1.0 + self.m_theta * np.cos(2 * np.pi * self.f_theta * self.t * self.dt)
        drive = self.P @ self.s                                   # resonance with field
        net = (g * (drive - self.J_inh * drive.mean() + self.bias)
               - self.beta * self.a
               + self.sigma_JN * self.rng.standard_normal(self.K))  # Johnson-Nyquist
        self.v = self.leak_v * self.v + net                       # integrate
        sp = (self.v > self.thr).astype(float)                    # threshold -> spike
        self.v = self.v * (1 - sp)                                # reset
        self.a = (self.a + sp) * np.exp(-self.dt / self.tau_a)    # adapt + decay
        self.s = self.field_leak * self.s + self.inject * (sp @ self.P)  # spikes write field
        self.s = self.s / (np.linalg.norm(self.s) + 1e-9)         # held standing wave
        self.t += 1
        return sp, self.s.copy(), g


# ============================================================
# DEMO 1 -- the two sides: silent held percept + sparse theta-locked spikes
# ============================================================
def demo_two_sides(seed=1):
    rng = np.random.default_rng(0)
    N, K = 400, 5
    P = np.array([(lambda v: (v - v.mean()) / np.linalg.norm(v - v.mean()))
                  (rng.standard_normal(N)) for _ in range(K)])
    eng = EphapticSpikingField(P, beta=6.0, thr=0.55, inject=0.18,
                               field_leak=0.985, sigma_JN=0.06, tau_a=0.18, seed=seed)
    eng.seed_field(P[0] + 0.3 * rng.standard_normal(N))
    steps = 4000
    OV = np.zeros((steps, K)); SP = np.zeros((steps, K))
    TH = np.zeros(steps); MOVE = np.zeros(steps); DOM = np.zeros(steps, int)
    prev = eng.s.copy()
    for t in range(steps):
        sp, s, g = eng.step()
        OV[t] = P @ s; SP[t] = sp; TH[t] = g
        MOVE[t] = np.linalg.norm(s - prev); prev = s.copy()
        DOM[t] = int(np.argmax(np.abs(P @ s)))
    return dict(OV=OV, SP=SP, TH=TH, MOVE=MOVE, DOM=DOM, K=K, dt=eng.dt, steps=steps,
                f_theta=eng.f_theta, m_theta=eng.m_theta)


# ============================================================
# DEMO 2 -- the hippocampal loop: emergent sweeps + alternation (non-circular)
# ============================================================
def demo_ring(beta, A_bias=0.9, seed=7):
    M = 120
    phi = np.linspace(0, 2 * np.pi, M, endpoint=False)
    heading = np.pi / 2
    P = np.array([np.exp(6.0 * np.cos(phi - phi[k])) for k in range(M)])
    P = P / np.linalg.norm(P, axis=1, keepdims=True)
    bias = np.exp(2.0 * np.cos(phi - heading)); bias = A_bias * bias / bias.max()
    eng = EphapticSpikingField(P, beta=beta, thr=0.5, inject=0.05, field_leak=0.96,
                               sigma_JN=0.04, tau_a=0.060, J_inh=0.8, bias=bias, seed=seed)
    eng.seed_field(np.exp(3.0 * np.cos(phi - heading)))
    steps = 4000
    R = np.zeros((steps, M)); TH = np.zeros(steps); DEC = np.zeros(steps)
    for t in range(steps):
        sp, s, g = eng.step()
        R[t] = s; TH[t] = g
        DEC[t] = np.angle(np.sum(s * np.exp(1j * phi)))
    return dict(R=R, TH=TH, DEC=DEC, phi=phi, heading=heading, M=M,
                dt=eng.dt, steps=steps, f_theta=eng.f_theta)


def wrap(x): return (x + np.pi) % (2 * np.pi) - np.pi
def cyc_off(dec, heading, f_theta, dt, T):
    return np.array([wrap(dec[int((c + 0.5) / f_theta / dt)] - heading)
                     for c in range(int(T * f_theta)) if int((c + 0.5) / f_theta / dt) < len(dec)])
def alt_score(off):
    s = np.sign(off)
    if len(s) < 3: return 0.0
    return np.mean([1.0 if (s[i] != s[i+1] and s[i+1] != s[i+2] and s[i] == s[i+2]) else 0.0
                    for i in range(len(s) - 2)])


# ============================================================
# RUN + VERIFY
# ============================================================
A = demo_two_sides()
T_A = A['steps'] * A['dt']
total_spk = A['SP'].sum()
sparsity = 100 * total_spk / (A['steps'] * A['K'])
spk_steps = A['SP'].sum(1) > 0
theta_hi = A['TH'] > 1.0 + 0.5 * A['m_theta']
lock = 100 * np.mean(theta_hi[spk_steps])
tr = np.array([A['DOM'][i] != A['DOM'][i-1] for i in range(1, A['steps'])])
nearT = np.zeros(A['steps'], bool)
for ti in np.where(tr)[0]: nearT[max(0, ti-3):ti+4] = True
dwell_v = A['MOVE'][1:][~nearT[1:]].mean()
trans_v = A['MOVE'][1:][nearT[1:]].mean()

ring_on = demo_ring(beta=1.5)
ring_off = demo_ring(beta=0.0)
off_on = cyc_off(ring_on['DEC'], ring_on['heading'], ring_on['f_theta'], ring_on['dt'], T_A)
off_off = cyc_off(ring_off['DEC'], ring_off['heading'], ring_off['f_theta'], ring_off['dt'], T_A)
deg_on, deg_off = np.degrees(np.mean(np.abs(off_on))), np.degrees(np.mean(np.abs(off_off)))
alt_on, alt_off = alt_score(off_on), alt_score(off_off)

print("=== DEMO 1: the two sides ===")
print(f"  spikes: {int(total_spk)} in {A['steps']}x{A['K']} slots  ->  sparsity {sparsity:.2f}%")
print(f"  theta-locking of spikes: {lock:.0f}%  (chance 50%)")
print(f"  field |ds|: DWELL {dwell_v:.4f}  vs  TRANSITION {trans_v:.4f}  -> silence ratio {trans_v/dwell_v:.0f}x")
print("=== DEMO 2: the hippocampal loop (non-circular) ===")
print(f"  adapt ON  (beta=1.5): sweep offset {deg_on:.1f} deg, alternation {alt_on:.2f}")
print(f"  adapt OFF (beta=0.0): sweep offset {deg_off:.1f} deg, alternation {alt_off:.2f}")


# ============================================================
# FIGURE
# ============================================================
BG="#0a0a12"; PAN="#12121e"; CRED="#ff3b6b"; CBLU="#2ec5ff"; CGRY="#6b6b85"; CYEL="#f5c542"; CGRN="#42f5a1"
plt.rcParams['font.family']='monospace'
fig=plt.figure(figsize=(15,9.4),facecolor=BG)
gs=GridSpec(2,3,figure=fig,hspace=0.46,wspace=0.30,top=0.89,bottom=0.07,left=0.06,right=0.975)
def axis(p,title,c=CBLU):
    a=fig.add_subplot(p); a.set_facecolor(PAN); a.set_title(title,color=c,fontsize=9.5,pad=6)
    a.tick_params(colors=CGRY,labelsize=7)
    for sp in a.spines.values(): sp.set_color("#23233a")
    return a
ttA=np.arange(A['steps'])*A['dt']

# (0,0) held content -- island overlaps over time
a=axis(gs[0,0],"SIDE A  ·  held content  (field resonance per island)",CGRN)
a.imshow(np.abs(A['OV'].T),aspect='auto',origin='lower',cmap='magma',
         extent=[0,T_A,-0.5,A['K']-0.5],vmin=0,vmax=0.9)
a.set_yticks(range(A['K'])); a.set_ylabel("spectral island",color=CGRY,fontsize=8)
a.set_xlabel("time (s)",color=CGRY,fontsize=8)
a.text(0.02,0.96,"one percept held, then switches",transform=a.transAxes,color='white',fontsize=7,va='top')

# (0,1) spike raster + theta clock
a=axis(gs[0,1],"SIDE B  ·  spikes  (sparse + theta-locked)",CYEL)
for k in range(A['K']):
    idx=np.where(A['SP'][:,k]>0)[0]
    a.plot(idx*A['dt'],np.full(len(idx),k),'|',color=CRED,ms=12,mew=1.6)
a2=a.twinx(); a2.plot(ttA,A['TH'],color=CBLU,lw=0.8,alpha=0.55)
a2.set_ylabel("theta gain",color=CBLU,fontsize=8); a2.tick_params(colors=CBLU,labelsize=6)
for sp in a2.spines.values(): sp.set_color("#23233a")
a.set_ylim(-0.6,A['K']-0.4); a.set_yticks(range(A['K']))
a.set_ylabel("island",color=CGRY,fontsize=8); a.set_xlabel("time (s)",color=CGRY,fontsize=8)
a.text(0.02,0.96,f"{sparsity:.2f}% sparse · {lock:.0f}% on theta peak",
       transform=a.transAxes,color='white',fontsize=7,va='top')

# (0,2) field velocity = the delta code
a=axis(gs[0,2],"the delta-code  ·  field velocity |ds/dt|",CRED)
a.plot(ttA,A['MOVE'],color=CGRY,lw=0.7,alpha=0.9)
a.plot(np.where(nearT,ttA,np.nan),np.where(nearT,A['MOVE'],np.nan),color=CRED,lw=0.9)
a.set_ylabel("|ds/dt|",color=CGRY,fontsize=8); a.set_xlabel("time (s)",color=CGRY,fontsize=8)
a.text(0.02,0.96,f"silent when held ({dwell_v:.4f})\nmoves at transition ({trans_v:.4f}) = {trans_v/dwell_v:.0f}x",
       transform=a.transAxes,color='white',fontsize=7,va='top')

# (1,0) ring standing wave, adaptation ON
a=axis(gs[1,0],"same engine, direction islands  ·  adaptation ON",CYEL)
R=ring_on['R']; M=ring_on['M']
a.imshow(np.roll(R.T,M//2,axis=0),aspect='auto',origin='lower',cmap='magma',
         extent=[0,T_A,-180,180])
a.axhline(0,color=CBLU,lw=1,ls='--',alpha=0.7)
a.set_ylabel("direction − heading (deg)",color=CGRY,fontsize=8); a.set_xlabel("time (s)",color=CGRY,fontsize=8)
a.text(0.02,0.96,"standing wave flips side each theta cycle",transform=a.transAxes,color='white',fontsize=7,va='top')

# (1,1) decoded offset ON vs OFF
a=axis(gs[1,1],"emergent theta sweeps  ·  ON vs OFF")
o_on=np.degrees(wrap(ring_on['DEC']-ring_on['heading']))
o_off=np.degrees(wrap(ring_off['DEC']-ring_off['heading']))
a.plot(ttA,o_off,color=CGRY,lw=1.0,alpha=0.9)
a.plot(ttA,np.where(o_on>=0,o_on,np.nan),color=CBLU,lw=1.2)
a.plot(ttA,np.where(o_on<0,o_on,np.nan),color=CRED,lw=1.2)
a.plot([],[],color=CBLU,lw=1.2,label=f"adapt ON  ({deg_on:.0f}°, alt {alt_on:.2f})")
a.plot([],[],color=CGRY,lw=1.2,label=f"adapt OFF ({deg_off:.0f}°, alt {alt_off:.2f})")
a.axhline(0,color="#33334d",lw=0.8); a.set_ylim(-110,110)
a.set_ylabel("offset (deg)",color=CGRY,fontsize=8); a.set_xlabel("time (s)",color=CGRY,fontsize=8)
a.legend(facecolor=PAN,edgecolor="#23233a",labelcolor='white',fontsize=6.5,loc='upper right')

# (1,2) verdict
a=fig.add_subplot(gs[1,2]); a.set_facecolor(PAN); a.axis('off')
for sp in a.spines.values(): sp.set_color("#23233a")
txt=("ONE ENGINE, TWO SIDES\n"
     "  field s  = held standing wave (content)\n"
     "  spikes   = sparse, theta-locked updates\n"
     "  coupling = via shared field only (ephaptic)\n\n"
     "DEMO 1 result\n"
     f"  spikes {sparsity:.2f}% sparse, {lock:.0f}% theta-locked\n"
     f"  field silent when held, moves {trans_v/dwell_v:.0f}x\n"
     f"  more at transitions = a clean delta-code\n\n"
     "DEMO 2  (non-circular, like the CAN test)\n"
     "  never told: sweep way / length / parity\n"
     f"  adapt ON : ~{deg_on:.0f}° sweeps, alt {alt_on:.2f}\n"
     f"  adapt OFF: ~{deg_off:.0f}° pinned, alt {alt_off:.2f}\n"
     "  -> sweeps + alternation EMERGE from beta\n\n"
     "NOT shown: that the held wave is felt;\n"
     "that thermal noise is the content medium.\n"
     "Those remain the bet, not the result.")
a.text(0.0,1.0,txt,transform=a.transAxes,color='white',fontsize=8.0,va='top',linespacing=1.5)

fig.suptitle("Ephaptic Spiking Field  ·  the held standing wave (content) and the sparse spikes (communication) in one engine",
             color='white',fontsize=11.5,y=0.955)
out="ephaptic_spiking_field.png"
plt.savefig(out,dpi=140,bbox_inches='tight',facecolor=BG); plt.close()
print("saved",out)
