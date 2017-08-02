def yfunc(t,par):
    import numpy as np
    yfunc = par[0]*t + par[1] - par[1]*np.exp(-par[2]*t)-par[3]
    return yfunc

def calc(a, b, c, d):
    import numpy as np
    import scipy.optimize as opt
    count = a.size
    time = np.zeros(count)
    for j in range (count):
        inp = [a[j],b[j],c[j],d]
        time[j] = opt.brentq(yfunc,0.,100.,args=inp)
    return time

def Discret(drops, timePar, dropPar, heatZ):
    import numpy as np
    velr, velz, posr, posz, radi = drops
    consA, consB, consD, consE, consF, consG = dropPar
    stepT= timePar
    count = velr.size
    #print radi
    for i in range (count):
        vrOld = velr[i]
        vzOld = velz[i]
        rzOld, rzInit = posz[i], posz[i]
        rrOld = posr[i]
        raOld = radi[i]
        while rzOld-rzInit < heatZ:
            lOld = consA/raOld**2
            sOld = consB/raOld**2
            consC = (9.8 - lOld)/sOld
            vOld = np.sqrt(vrOld**2+vzOld**2)
            raNew = raOld - consC*consG/raOld**2 - consD*consE*consF*np.sqrt(consG)*np.power(raOld,-7./6.)*np.sqrt(vOld)
            vrNew = vrOld - vrOld*sOld*stepT
            vzNew = vzOld - (sOld*vzOld - 9.8 + lOld)*stepT
            rrNew = rrOld + vrOld*stepT
            rzNew = rzOld + vzOld*stepT
            #print raNew, rzNew, vOld        
            if np.isnan(raNew) or raNew < 1e-6:
                velr[i] = vrOld
                velz[i] = vzOld
                posz[i] = rzOld
                posr[i] = np.nan
                radi[i] = np.nan
                break
            else:
                raSt, vrSt, vzSt, rrSt, rzSt = raOld, vrOld, vzOld, rrOld, rzOld
                raOld, vrOld, vzOld, rrOld, rzOld = raNew, vrNew, vzNew, rrNew, rzNew
        if np.isnan(raNew) or raNew < 1e-6:        
            velr[i] = vrOld
            velz[i] = vzOld
            posz[i] = rzOld
            posr[i] = np.nan
            radi[i] = np.nan
        else:
            velr[i] = vrSt
            velz[i] = vzSt
            posz[i] = rzSt
            posr[i] = rrSt
            radi[i] = raSt
    return velr, velz, posr, posz, radi
  
if __name__ ==  "__main__":
    import numpy.random as rdn
    import numpy as np
    import dispy
    import time as tt
    import pixel, outtiff
    import warnings
    #SPRAY PARAMETERS
    NozzS = 0.16
    radiusC = NozzS*np.tan(6*np.pi/180)
    AreaC = np.pi*radiusC**2
    volum = 2e-6
    avrad = 25e-6
    volpa = 4*np.pi*np.power(avrad,3)/3
    numpa = volum/volpa
    partR = 1e5
    partI = int(partR)
    PresN = 1e5
    DensD = 1.03e3
    NozzV = np.sqrt(2*PresN/DensD)
    # CIRCULAR DISTRIBUTION?
    #nran = rdn.random(partI)
    #ranArea = rdn.random(partI)*AreaC*0.01
    ranArea = np.sqrt(rdn.random(partI))*radiusC
    #ranAngl = np.arctan((np.sqrt(ranArea/np.pi))/NozzS)
    ranAngl = np.arctan(ranArea/NozzS)
    #vr0 = NozzV*np.sin(6*np.pi*nran/180)
    vr0 = NozzV*np.sin(ranAngl)
    vv0 = np.sqrt(NozzV**2-vr0**2)

    #DROPLET TRANSPORT
    HeatZ = 5e-3
    ViscA = 18.6e-6
    ViscD = 1.37e-3
    TherA = 0.024
    TherD = 0.159
    DensA = 1.1839
    TempA = 25.+273
    TempS = 50.+273
    CoolZ = (NozzS - HeatZ)
    VariT = TempS - TempA
    R = 8.3144621
    nAvog = 6.022e23
    variP = 67*(TempS-TempA)
    molD = 88.11e-3
    consD = molD*variP/(DensD*R*TempS)
    consE = 0.276*np.sqrt(2*DensA/ViscA)
    consF = np.power(ViscA/DensA,1./3.)
    consG = R*TempS/(6*np.pi*ViscD*nAvog)
    nran = rdn.random(partI)
    rmax = 40e-6
    rmin = 15e-6
    radi = np.power(nran*(np.power(rmax,-1./3)-np.power(rmin,-1./3.)) + np.power(rmin,-1./3.),-3.)
    consA = 27.*ViscA**2.*TherA*VariT/(4.*DensA*DensD*TempA*(2.*TherA+TherD)*NozzS)
    l = consA/radi**2
    consB = 9.*ViscA/(2.*DensD)
    s = consB/radi**2
    cons1 = (9.8-l)/s
    cons2 = (vv0 - cons1)/s
    #temp = linspace(0,0.1,1001);
    #y = cons1*temp + cons2 - cons2*exp(-s*temp)-0.2;
    # TIME FLIGHT
    time = np.zeros(partI)

    start = tt.clock()
    #CLUSTER1: 2 CORES; CLUSTER2 : 8 CORES
    coreN = 12
    cluster = dispy.JobCluster(calc,depends=[yfunc])
    dv = np.linspace(0,partR-1,coreN+1)
    dv = dv.astype('int32')
    #print dv
    jobs = []
    #print par[3]
    for i in range (coreN):
        a, b = dv[i], dv[i+1]
        job = cluster.submit(cons1[a:b],cons2[a:b],s[a:b],CoolZ)
        job.id = i
        jobs.append(job)
    for job in jobs:
        a, b = dv[job.id], dv[job.id+1]
        time[a:b] = job()
    cluster.stats()
    cluster.close()
    
    #print time
    elapsed = tt.clock()-start
    #print elapsed

    #RADIAL DISPLACEMENT
    posR1 = vr0/s - vr0*np.exp(-s*time)/s
    posR = np.ones(partI)*posR1

    #VERTICAL DISPLACEMENT BEFORE HEAT ZONE
    posZ = CoolZ*np.ones(partI)

    #VELOCITTY BEFORE HEAT ZONE
    velR = vr0*np.exp(-s*time)
    velZ = (vv0-cons1)*np.exp(-s*time)+cons1

    #TRANSPORT IN HEAT ZONE
    start = tt.clock()
    cluster2 = dispy.JobCluster(Discret)
    jobs = []
    for i in range (10):
        a, b = dv[i], dv[i+1]
        drops = [velR[a:b], velZ[a:b], posR[a:b], posZ[a:b], radi[a:b]]
        dropPar = [consA, consB, consD, consE, consF, consG]
        timePar = 1e-6
        job = cluster2.submit(drops,timePar,dropPar,HeatZ)
        job.id = i
        jobs.append(job)
    for job in jobs:
        a, b = dv[job.id], dv[job.id+1]
        velR[a:b], velZ[a:b], posR[a:b], posZ[a:b], radi[a:b] = job()
    
    cluster2.stats()
    cluster2.close()

    elapsed = tt.clock()-start
    #print divmod(elapsed,60)

    #LANDING COORDINATES
    aran = 2.*np.pi*rdn.random(partI)
    xdrop = posR*np.cos(aran)
    ydrop = posR*np.sin(aran)


    #PIXELIZATION
    #image = pixel.pixelization(partI,xdrop,ydrop,radi,[-0.02,0.02])
    #outtiff.tifff(image.astype('uint16'),'sim.tif','sim')
    #tupi = cm.bone._segmentdata
    #cmap = mcol.LinearSegmentedColormap('name',tupi,gamma=1.0)
    #plt.imshow(image,cmap=cmap, interpolation='none')
    #plt.show()

    # WRITING TEXTFILE
    index = []
    for i in range (partI):
        logn = np.isnan(xdrop[i]) or np.isnan(xdrop[i])
        if logn:
            index.append(i)
    xr = np.delete(xdrop,index)
    del xdrop
    yr = np.delete(ydrop,index)
    del ydrop
    rr = np.delete(radi,index)
    del radi
    np.savetxt('1e5-15-40u-x100-6d.out', (xr,yr,rr))
 





    
