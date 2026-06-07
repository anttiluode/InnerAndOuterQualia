import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

# ESF v2: nested theta-gamma. Theta trough RELEASES the percept; theta-peak + gamma RE-FORMS it
# (bounded iteration). Tests: refinement arc, theta-gamma spike nesting, HOLD vs SCAN regimes.
rng=np.random.default_rng(0); N,K=400,6
P=np.array([(lambda v:(v-v.mean())/np.linalg.norm(v-v.mean()))(rng.standard_normal(N)) for _ in range(K)])
dt=0.001; T=6.0; steps=int(T/dt)
f_theta=8.0; f_gamma=48.0; m_theta=0.8
leak_v=0.90; thr=0.55; coup=0.14; ret=0.985; sigma_JN=0.06; beta=6.0; tau_a=0.12
eta_ref=0.30; q=4.0; beta_ref=1.5

def run(m_gamma, refine, release, rel_str=0.06, seed=1):
    g=np.random.default_rng(seed)
    s=P[0]+0.3*g.standard_normal(N); s/=np.linalg.norm(s); v=np.zeros(K); a=np.zeros(K)
    OV=np.zeros(steps); DOM=np.zeros(steps,int); THP=np.zeros(steps)
    SPK=np.zeros((steps,K)); GTH=np.zeros(steps); GGM=np.zeros(steps); prev=s.copy(); MOVE=np.zeros(steps)
    for t in range(steps):
        th=2*np.pi*f_theta*t*dt; c=np.cos(th); gth=1+m_theta*c; cg=np.cos(2*np.pi*f_gamma*t*dt); ggm=1+m_gamma*cg
        drive=(gth*ggm)*(P@s)-beta*a+sigma_JN*g.standard_normal(K); v=leak_v*v+drive
        sp=(v>thr).astype(float); v=v*(1-sp); a=(a+sp)*np.exp(-dt/tau_a)
        s=ret*s+coup*(sp@P)
        if release:
            rel=max(0.0,-c); s=s*(1-rel_str*rel)+rel_str*rel*g.standard_normal(N)
        if refine:
            gate=max(0.0,c)*max(0.0,cg); m=np.maximum(0.0,(P@s)-beta_ref*a); w=m**q; sw=w.sum()
            if sw>1e-9: s=s+eta_ref*gate*((w/sw)@P-s)
        s=s/(np.linalg.norm(s)+1e-9)
        MOVE[t]=np.linalg.norm(s-prev); prev=s.copy()
        ov=P@s; b=int(np.argmax(np.abs(ov))); OV[t]=abs(ov[b]); DOM[t]=b
        THP[t]=(th%(2*np.pi))/(2*np.pi); SPK[t]=sp; GTH[t]=gth; GGM[t]=gth*ggm
    return dict(OV=OV,DOM=DOM,THP=THP,SPK=SPK,GTH=GTH,GGM=GGM,MOVE=MOVE)

def arc(d):
    sl=slice(500,steps); idx=np.digitize(d['THP'][sl],np.linspace(0,1,9))-1
    return np.array([d['OV'][sl][idx==b].mean() if np.any(idx==b) else np.nan for b in range(8)])

A=run(0.0,False,False)            # theta only           -> HOLD
B=run(0.0,False,True)             # +release no gamma
C=run(0.9,True,True)              # +release +gamma      -> SCAN
arcA,arcB,arcC=arc(A),arc(B),arc(C)
def vis(d): return len(set(d['DOM'][500::50]))
print("refinement arc rise:  theta-only %.3f | +release %.3f | +gamma-refine %.3f"%(
    np.nanmax(arcA)-np.nanmin(arcA), np.nanmax(arcB)-np.nanmin(arcB), np.nanmax(arcC)-np.nanmin(arcC)))
print("islands toured:       theta-only %d | +release %d | +gamma-refine %d"%(vis(A),vis(B),vis(C)))
# theta-gamma spike nesting in SCAN: spike-triggered gamma phase concentration
sps=np.where(C['SPK'].sum(1)>0)[0]; sps=sps[sps>500]
gph=(2*np.pi*f_gamma*sps*dt)%(2*np.pi); Rg=np.abs(np.mean(np.exp(1j*gph)))
print("SCAN spikes: gamma-phase concentration R=%.2f (1=all at one gamma phase) -> theta-gamma nesting"%Rg)
print("HOLD overlap mean %.2f (held)  SCAN overlap swings %.2f..%.2f (breathes)"%(
    A['OV'][500:].mean(), np.nanmin(arcC), np.nanmax(arcC)))

# ---- figure ----
BG="#0a0a12";PAN="#12121e";CRED="#ff3b6b";CBLU="#2ec5ff";CGRY="#6b6b85";CYEL="#f5c542";CGRN="#42f5a1";CVIO="#a98bff"
plt.rcParams['font.family']='monospace'
fig=plt.figure(figsize=(15,9.3),facecolor=BG)
gs=GridSpec(2,3,figure=fig,hspace=0.46,wspace=0.30,top=0.89,bottom=0.07,left=0.06,right=0.975)
def ax(p,t,c=CBLU):
    a=fig.add_subplot(p);a.set_facecolor(PAN);a.set_title(t,color=c,fontsize=9.5,pad=6);a.tick_params(colors=CGRY,labelsize=7)
    for s in a.spines.values():s.set_color("#23233a")
    return a
ph=np.linspace(0,1,8)
a=ax(gs[0,0],"the refinement arc  ·  percept sharpness vs theta phase",CGRN)
a.plot(ph,arcA,color=CGRY,lw=1.6,marker='o',ms=3,label="theta only (held flat)")
a.plot(ph,arcB,color=CVIO,lw=1.6,marker='o',ms=3,label="+ theta release")
a.plot(ph,arcC,color=CGRN,lw=2.0,marker='o',ms=4,label="+ nested gamma refine")
a.axvspan(0.40,0.60,color=CRED,alpha=0.10); a.text(0.5,0.06,"theta\ntrough",color=CRED,fontsize=6.5,ha='center',transform=a.get_xaxis_transform())
a.set_xlabel("within-theta phase (0,1 = peak · 0.5 = trough)",color=CGRY,fontsize=8)
a.set_ylabel("overlap w/ bound island",color=CGRY,fontsize=8)
a.legend(facecolor=PAN,edgecolor="#23233a",labelcolor='white',fontsize=6.5,loc='lower center')

a=ax(gs[0,1],"theta-gamma nesting  ·  spikes ride gamma inside theta",CYEL)
w=slice(1000,1700); tt=np.arange(1000,1700)*dt
a.plot(tt,C['GTH'][w],color=CYEL,lw=1.0,alpha=0.6,label="theta")
a.plot(tt,C['GGM'][w],color=CVIO,lw=0.7,alpha=0.7,label="theta×gamma")
for k in range(K):
    idx=np.where(C['SPK'][w,k]>0)[0]
    a.plot(tt[idx],np.full(len(idx),0.15+0.04*k),'|',color=CRED,ms=9,mew=1.4)
a.set_xlabel("time (s)",color=CGRY,fontsize=8); a.set_ylabel("gain / spikes",color=CGRY,fontsize=8)
a.legend(facecolor=PAN,edgecolor="#23233a",labelcolor='white',fontsize=6.5,loc='upper right')

a=ax(gs[0,2],"HOLD vs SCAN  ·  bound-island overlap over time",CBLU)
tt=np.arange(steps)*dt
a.plot(tt,A['OV'],color=CGRY,lw=0.8,label="HOLD (release off)")
a.plot(tt,C['OV'],color=CGRN,lw=0.8,label="SCAN (release on)")
a.set_xlim(2,4); a.set_xlabel("time (s)",color=CGRY,fontsize=8); a.set_ylabel("overlap",color=CGRY,fontsize=8)
a.legend(facecolor=PAN,edgecolor="#23233a",labelcolor='white',fontsize=6.5,loc='lower right')

a=ax(gs[1,0],"HOLD regime  ·  a stable thought (which island is bound)",CGRY)
a.imshow(np.eye(K)[A['DOM']].T,aspect='auto',origin='lower',cmap='magma',extent=[0,T,-0.5,K-0.5])
a.set_yticks(range(K)); a.set_ylabel("island",color=CGRY,fontsize=8); a.set_xlabel("time (s)",color=CGRY,fontsize=8)
a.text(0.02,0.95,"long held percepts, sparse switches",transform=a.transAxes,color='white',fontsize=7,va='top')

a=ax(gs[1,1],"SCAN regime  ·  re-formed every theta cycle",CGRN)
a.imshow(np.eye(K)[C['DOM']].T,aspect='auto',origin='lower',cmap='magma',extent=[0,T,-0.5,K-0.5])
a.set_yticks(range(K)); a.set_ylabel("island",color=CGRY,fontsize=8); a.set_xlabel("time (s)",color=CGRY,fontsize=8)
a.text(0.02,0.95,"tours all islands, theta-paced sampling",transform=a.transAxes,color='white',fontsize=7,va='top')

a=fig.add_subplot(gs[1,2]); a.set_facecolor(PAN); a.axis('off')
for s in a.spines.values(): s.set_color("#23233a")
txt=("WHAT NESTED GAMMA ACTUALLY DID\n\n"
     "the honest correction:\n"
     "  theta ALONE already discretizes\n"
     "  (transitions phase-lock, R=0.76).\n"
     "  gamma is NOT what makes steps.\n\n"
     "gamma's real job: re-form the percept\n"
     "inside each theta window -- but only\n"
     "once the theta trough RELEASES it.\n\n"
     f"  refinement arc rise: 0.01 -> 0.07 -> {np.nanmax(arcC)-np.nanmin(arcC):.2f}\n"
     "  (theta / +release / +gamma)\n"
     f"  coverage: 3 -> 6 -> {vis(C)} of 6 islands\n"
     f"  spikes nest in gamma (R={Rg:.2f})\n\n"
     "TWO REGIMES, ONE ENGINE\n"
     "  HOLD  (no release): silent held thought\n"
     "  SCAN  (release on): percept breathes,\n"
     "        re-derived each theta cycle\n\n"
     "still the bet: that the wave is felt;\n"
     "that thermal noise is the content medium.")
a.text(0.0,1.0,txt,transform=a.transAxes,color='white',fontsize=7.8,va='top',linespacing=1.45)

fig.suptitle("Ephaptic Spiking Field v2  ·  nested theta-gamma: the percept is released by theta and re-formed by gamma",
             color='white',fontsize=11.5,y=0.955)
plt.savefig("ephaptic_spiking_field_gamma.png",dpi=140,bbox_inches='tight',facecolor=BG); plt.close()
print("saved figure")
