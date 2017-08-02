% get the list of files for reference
fpath = 'C:\Users\ref\';
files = dir( fullfile(fpath,'*.txt') );
files = strcat(fpath,{files.name});

% read data from all files and store in cell array
xref = 0;
for i=1:numel(files)
	xref = csvread(files{i}) + xref;
end
% mean value of reference
xref = xref/numel(files);
%%
% get the list of files for interference
fpath = 'C:\Users\interf\';
files = dir( fullfile(fpath,'*.txt') );
files = strcat(fpath,{files.name});
%%
tot_vx=zeros(1,2);
ne=0;
%%
% read data from each file and store in an array
for nf=1:numel(files)
    %% 
    %select the crop region and their dimensions 
    disp(nf);
    %%
    if nf==1;
    [thepath, thename] = fileparts(files{nf});
    xnew = csvread(files{nf});
    xnew = xnew - xref;
    % rect = (minx miny width height)
    img=imagesc(xnew);
    [I2 rect] = imcrop(img);
    rect=int16(rect);
    end
    % Setting up the pixel matrix for the pattern
    pattern = zeros(rect(4),rect(3));
    for a=1:rect(4)
        for b=1:rect(3)
            pattern(a,b)= xnew(rect(2)+a,rect(1)+b);
        end
    end
    %%
    % Find the phase and the intensity
    ne=ne+1;
    im=zeros(size(pattern));
    phase=zeros(size(pattern));
    thr1=0.02;
	[im(:,:),phase(:,:)] = phase2(pattern(:,:),thr1);
	%% 
    % What region are the vortices on?
    if nf==1
    img=imagesc(phase);
    colormap(bone);
    [I5 rec] = imcrop(img);
    rec=int16(rec);
    end
    % Find vortices
    [xyt] = vducrop3(phase(:,:),rec);
    cvx = ones(500,1);
    cax = -1.*ones(500,1);
    tot_vx(ne,1)=sum(xyt(:,3)==cvx);
    tot_vx(ne,2)=sum(xyt(:,3)==cax);
    	%%
    % Display data on the screen and save as pdf
    h=8;
    [x,y] = meshgrid(1:h:length(phase(1,:)),1:h:length(phase(:,1)));
    vek=zeros(size(x));
    for a=1:h:length(phase(:,1))
        for b=1:h:length(phase(1,:))
            vek((a-1)/h+1,(b-1)/h+1)=phase(a,b);
        end
    end
    
    [FX, FY]=gradient(vek(:,:),h,h);
    
    for a=1:h:length(phase(:,1))
        for b=1:h:length(phase(1,:))
            a1=(a-1)/h+1;
            b1=(b-1)/h+1;
            if FX(a1,b1)>=0.2 || FX(a1,b1)<=-0.2,FX(a1,b1)=NaN; end;
            if FY(a1,b1)>=0.2 || FY(a1,b1)<=-0.2,FY(a1,b1)=NaN; end;
        end
    end
    
	figure()
        imagesc(phase(:,:))
        colormap(bone)
        set(gca,'XTick',0:68.333333:615)
        set(gca,'XTickLabel',0:10:90)
        set(gca,'YTick',0:68.333333:615)
        set(gca,'YTickLabel',0:10:90)
        xlabel('X-Position (\mum)')
        ylabel('Y-Position (\mum)')
        hold on
        for m=1:100,
            if xyt(m,3)>0,
                plot(xyt(m,2),xyt(m,1),'rs','MarkerSize',10)
            else
                plot(xyt(m,2),xyt(m,1),'gs','MarkerSize',10)
            end
        end
        quiver(x,y,FX,FY,0.8,'r');
        hold off
        filename = [thename,'_phase','.pdf'];
        saveas(gcf,filename);
        close(gcf);
        %%
        figure();
        imagesc(im(:,:));
        colormap(bone);
        set(gca,'XTick',0:68.333333:615)
        set(gca,'XTickLabel',0:10:90)
        set(gca,'YTick',0:68.333333:615)
        set(gca,'YTickLabel',0:10:90)
        xlabel('X-Position (\mum)')
        ylabel('Y-Position (\mum)')
        hold on
        for m=1:100,
            if xyt(m,3)>0,
                plot(xyt(m,2),xyt(m,1),'ro','MarkerSize',10)
            else
                plot(xyt(m,2),xyt(m,1),'go','MarkerSize',10)
            end
        end
        hold off
        filename = [thename,'_intensity','.pdf'];
        saveas(gcf,filename);
        close all;
end
%%
%[error_vx error_ax] = std(tot_vx,0,1);
error = std(tot_vx)/sqrt(ne);
means = mean(tot_vx);
filename = [thename,'_results','.txt'];
fid = fopen(filename, 'w');
fprintf(fid, 'Results\n');
fprintf(fid, '%g  %g\n', tot_vx');
fprintf(fid, '\n Standard Error\n');
fprintf(fid, '%2.5f  %2.5f\n', error);
fprintf(fid, '\n Mean\n');
fprintf(fid, '%2.5f  %2.5f\n', means);
fclose(fid);



