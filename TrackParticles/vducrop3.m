% xyt --> vortices

function [xyt] = vducrop3(phase,rec)
	xyt=zeros(500,3);
    %L=0;
    %N=0;
	n=1;
	mink=min(min(phase));
	maxk=max(max(phase));
	phase=(phase-mink)/(maxk-mink);
       
    %%
    %contrast=del2(phase);
    %mink=min(min(contrast));
	%maxk=max(max(contrast));
	%contrast=(contrast-mink)/(maxk-mink);
    neo1=int16(10000.*phase);
    neo=neo1;
    neo2=neo;
    %%
    for j=1:length(neo(1,:))
        for i=1:length(neo(:,1))
            if neo(i,j)< 2300
                neo(i,j) = 1;
            end
            if neo(i,j)> 8000
                neo(i,j) = 4;
            end
            if neo(i,j)<= 8000 && neo(i,j)> 5000
                neo(i,j) = 3;
            end
            if neo(i,j)<= 5000 && neo(i,j)>= 2300
                neo(i,j) = 3;
            end
        end
    end
    
    for j=1:length(neo(1,:))
        for i=1:length(neo(:,1))
            if neo1(i,j)< 2300
                neo2(i,j) = 1;
            end
            if neo1(i,j)> 8000
                neo2(i,j) = 4;
            end
            if neo1(i,j)<= 8000 && neo1(i,j)> 5000
                neo2(i,j) = 1;
            end
            if neo1(i,j)<= 5000 && neo1(i,j)>= 2300
                neo2(i,j) = 1;
            end
        end
    end
    neo2=int8(neo2./4);
    %%
	% matricess of vorrtices and antivortices
	m1=[4 1; 3 3];
    m2=[4 1; 4 3];
	m3=[4 1; 3 1];
  	vx1 = cat(3,m1,m2,m3);
	vx2 = cat(3,rot90(m1),rot90(m2),rot90(m3));
	vx3 = cat(3,rot90(m1,2),rot90(m2,2),rot90(m3,2));
	vx4 = cat(3,rot90(m1,3),rot90(m2,3),rot90(m3,3));
	ax1 = cat(3,m1',m2',m3');
	ax2 = cat(3,rot90(m1)',rot90(m2)',rot90(m3)');
	ax3 = cat(3,rot90(m1,2)',rot90(m2,2)',rot90(m3,2)');
	ax4 = cat(3,rot90(m1,3)',rot90(m2,3)',rot90(m3,3)');
    fisb = [1 1 1; 1 0 1; 1 1 1];
    fisw = 1-1.*fisb;
    
    for i=rec(2):rec(2)+rec(4)
        for j=rec(1):rec(1)+rec(3)
            m6 = [neo(i-1,j-1) neo(i-1,j); neo(i,j-1) neo(i,j)];
            % top bottom left right
            fcb = [neo(i-1,j-1) neo(i-1,j) neo(i-1,j+1); neo(i,j-1) neo(i,j) neo(i,j+1); neo(i+1,j-1) neo(i+1,j) neo(i+1,j+1)];
            fcb = int8(fcb./4);
            ftb = [neo(i-2,j-1) neo(i-2,j) neo(i-2,j+1); neo(i-1,j-1) neo(i-1,j) neo(i-1,j+1); neo(i,j-1) neo(i,j) neo(i,j+1)];
            ftb = int8(ftb./4);
            fbb = [neo(i,j-1) neo(i,j) neo(i,j+1); neo(i+1,j-1) neo(i+1,j) neo(i+1,j+1); neo(i+2,j-1) neo(i+2,j) neo(i+2,j+1)];
            fbb = int8(fbb./4);
            flb = [neo(i-1,j-2) neo(i-1,j-1) neo(i-1,j); neo(i,j-2) neo(i,j-1) neo(i,j); neo(i+1,j-2) neo(i+1,j-1) neo(i+1,j)];
            flb = int8(flb./4);
            frb = [neo(i-1,j) neo(i-1,j+1) neo(i-1,j+2); neo(i,j) neo(i,j+1) neo(i,j+2); neo(i+1,j) neo(i+1,j+1) neo(i+1,j+2)];
            frb = int8(frb./4);
            % corners
            ctlb = [neo(i-2,j-2) neo(i-2,j-1) neo(i-2,j); neo(i-1,j-2) neo(i-1,j-1) neo(i-1,j); neo(i,j-2) neo(i,j-1) neo(i,j)];
            ctlb = int8(ctlb./4);
            ctrb = [neo(i-2,j) neo(i-2,j+1) neo(i-2,j+2); neo(i-1,j) neo(i-1,j+1) neo(i-1,j+2); neo(i,j) neo(i,j+1) neo(i,j+2)];
            ctrb = int8(ctrb./4);
            cblb = [neo(i,j-2) neo(i,j-1) neo(i,j); neo(i+1,j-2) neo(i+1,j-1) neo(i+1,j); neo(i+2,j-2) neo(i+2,j-1) neo(i+2,j)];
            cblb = int8(cblb./4);
            cbrb = [neo(i,j) neo(i,j+1) neo(i,j+2); neo(i+1,j) neo(i+1,j+1) neo(i+1,j+2); neo(i+2,j) neo(i+2,j+1) neo(i+2,j+2)];
            cbrb = int8(cbrb./4);
            % top bottom left right
            fcw = [neo2(i-1,j-1) neo2(i-1,j) neo2(i-1,j+1); neo2(i,j-1) neo2(i,j) neo2(i,j+1); neo2(i+1,j-1) neo2(i+1,j) neo2(i+1,j+1)];
            ftw = [neo2(i-2,j-1) neo2(i-2,j) neo2(i-2,j+1); neo2(i-1,j-1) neo2(i-1,j) neo2(i-1,j+1); neo2(i,j-1) neo2(i,j) neo2(i,j+1)];
            fbw = [neo2(i,j-1) neo2(i,j) neo2(i,j+1); neo2(i+1,j-1) neo2(i+1,j) neo2(i+1,j+1); neo2(i+2,j-1) neo2(i+2,j) neo2(i+2,j+1)];
            flw = [neo2(i-1,j-2) neo2(i-1,j-1) neo2(i-1,j); neo2(i,j-2) neo2(i,j-1) neo2(i,j); neo2(i+1,j-2) neo2(i+1,j-1) neo2(i+1,j)];
            frw = [neo2(i-1,j) neo2(i-1,j+1) neo2(i-1,j+2); neo2(i,j) neo2(i,j+1) neo2(i,j+2); neo2(i+1,j) neo2(i+1,j+1) neo2(i+1,j+2)];
            % corners
            ctlw = [neo2(i-2,j-2) neo2(i-2,j-1) neo2(i-2,j); neo2(i-1,j-2) neo2(i-1,j-1) neo2(i-1,j); neo2(i,j-2) neo2(i,j-1) neo2(i,j)];
            ctrw = [neo2(i-2,j) neo2(i-2,j+1) neo2(i-2,j+2); neo2(i-1,j) neo2(i-1,j+1) neo2(i-1,j+2); neo2(i,j) neo2(i,j+1) neo2(i,j+2)];
            cblw = [neo2(i,j-2) neo2(i,j-1) neo2(i,j); neo2(i+1,j-2) neo2(i+1,j-1) neo2(i+1,j); neo2(i+2,j-2) neo2(i+2,j-1) neo2(i+2,j)];
            cbrw = [neo2(i,j) neo2(i,j+1) neo2(i,j+2); neo2(i+1,j) neo2(i+1,j+1) neo2(i+1,j+2); neo2(i+2,j) neo2(i+2,j+1) neo2(i+2,j+2)];
            
            if isequal(fcb,fisb)|| isequal(fcw,fisw)|| isequal(flw,fisw)|| isequal(frw,fisw)|| ...
                    isequal(ftw,fisw)|| isequal(fbw,fisw)|| isequal(flb,fisb)|| isequal(frb,fisb)|| ...
                    isequal(ftb,fisb)|| isequal(fbb,fisb)|| isequal(ctlb,fisb)|| isequal(ctrb,fisb)|| ...
                    isequal(cblb,fisb)|| isequal(cbrb,fisb)|| isequal(ctlw,fisw)|| isequal(ctrw,fisw)|| ...
                    isequal(cblw,fisw)|| isequal(cbrw,fisw)
                continue,
            else
            for z=1:3
                if isequal(m6,vx1(:,:,z))||isequal(m6,vx2(:,:,z))||isequal(m6,vx3(:,:,z))||isequal(m6,vx4(:,:,z))
                    xyt(n,1)=i;
                    xyt(n,2)=j;
                    xyt(n,3)=-1;
                    n=n+1;
                end
            end
            for z=1:3
                if isequal(m6,ax1(:,:,z))||isequal(m6,ax2(:,:,z))||isequal(m6,ax3(:,:,z))||isequal(m6,ax4(:,:,z))
                    xyt(n,1)=i;
                    xyt(n,2)=j;
                    xyt(n,3)=1;
                    n=n+1;
                end
            end
            end
        end   
    end
end
