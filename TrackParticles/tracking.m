% get the list of files for reference
fpath = 'C:\Users\Lab\DATA_test\';
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
fpath = 'C:\Users\Lab\DATA_test\';
files = dir( fullfile(fpath,'*.txt') );
files = strcat(fpath,{files.name});
%%
tot=numel(files);
todo=[];
vec = [0 0 0];
%%
% read data from each file and store in an array
for nf=1:tot
    disp(nf);
    %%
    xnew = csvread(files{nf}); 
    if nf==1;
    % rect = (minx miny width height)
    img=imagesc(xnew);
    [~, rect] = imcrop(img);
    rect=int16(rect);
    end
    xnew = xnew - xref;
    % Setting up the pixel matrix for the pattern
    pattern = zeros(rect(4),rect(3));
    for a=1:rect(4)
        for b=1:rect(3)
            pattern(a,b)= xnew(rect(2)+a,rect(1)+b);
        end
    end
    %%
    % Find the phase and the intensity
    im=zeros(size(pattern));
    phase=zeros(size(pattern));
	[im(:,:),phase(:,:),vec(:,:)] = fase(pattern(:,:),vec,nf);
	%% 
    % What region are the vortices on?
    if nf==1
    img=imagesc(phase);
    colormap(bone);
    [~, rec] = imcrop(img);
    rec=int16(rec);
    end
    % Find vortices
    [xyt] = vducrop3(phase(:,:),rec);
    todo=cat(3,todo,xyt);
    %%
    % Plotting
    [thepath, thename] = fileparts(files{nf});
    hayley=figure;
    subplot(1,2,1);
    imagesc(phase(:,:))
    colormap(bone)
    %whitebg([1 1 0]);
    set(gca, 'XColor', 'g');
    set(gca, 'YColor', 'g');
    set(gca,'XTick',0:68.333333:615)
    set(gca,'XTickLabel',0:10:90)
    set(gca,'YTick',0:68.333333:615)
    set(gca,'YTickLabel',0:10:90)
    xlabel('X-Position (\mum)')
    ylabel('Y-Position (\mum)')
    hold on
    for m=1:100,
        if xyt(m,3)>0,
            plot(xyt(m,2),xyt(m,1),'rs','MarkerSize',10,'LineWidth',2)
        else
            plot(xyt(m,2),xyt(m,1),'bs','MarkerSize',10,'LineWidth',2)
        end
    end
    hold off
    subplot(1,2,2);
    imagesc(im(:,:));
    set(gca, 'XColor', 'g');
    set(gca, 'YColor', 'g');
    set(gca,'XTick',0:68.333333:615)
    set(gca,'XTickLabel',0:10:90)
    set(gca,'YTick',0:68.333333:615)
    set(gca,'YTickLabel',0:10:90)
    xlabel('X-Position (\mum)')
    ylabel('Y-Position (\mum)')
    hold on
    for m=1:100,
        if xyt(m,3)>0,
            plot(xyt(m,2),xyt(m,1),'ro','MarkerSize',10,'LineWidth',2)
        else
            plot(xyt(m,2),xyt(m,1),'bo','MarkerSize',10,'LineWidth',2)
        end
    end
    hold off
    truesize(hayley);
    iname=sprintf('plot_%03d.png', nf);
    set(hayley,'PaperPositionMode','auto')
    set(gcf, 'color', 'black');
    set(hayley, 'InvertHardCopy', 'off');
    print(hayley,'-dpng', iname);
    %%
    M(:,nf) = getframe(hayley);
    close(hayley);
end 

%% my great film
fr = 10;
mov = VideoWriter('movie1.avi');
mov.FrameRate = 10;
mov.Quality = 50;
open(mov);
for nf0=1:fr*tot
  nf=ceil(nf0/fr);  
  currFrame = M(:,nf);
  writeVideo(mov,currFrame);
end
close(mov);

%%
%{
d=zeros(500,500);
vec0=[0 0];
vec1=[todo(:,1,1) todo(:,2,1)];
vec2=[todo(:,1,2) todo(:,2,2)];
% I want only vortices
for h=1:500
    if todo(h,3,1)~=-1
        vec1(h,:)=vec0;
    end
end
for h=1:500
    if todo(h,3,2)~=-1
        vec2(h,:)=vec0;
    end
end
% All possible permutations
for l=1:500
for i=1:500   
if isequal(vec2(i,:),vec0) || isequal(vec1(l,:),vec0)
    continue,
end
d(l,i)=norm(vec2(i,:)-vec1(l,:));
end
end
%%
for l=1%:500
    
    dmin=min(d(:,l));
    z=1;
    while dmin~=d(z,l)
    z=z+1;
    end
end
%}

%%
y0=[];
x0=[];
figure();
imagesc(im(:,:));
colormap(bone);
hold on
for m=1:3
    col=[m/3 0.5 1];
    lo=length(todo(m,1,:));
    for i=1:lo
        y0(i,1)=todo(m,2,i);
        x0(i,1)=todo(m,1,i);
    end
%%
    if xyt(m,3)>0,
        plot(y0,x0,'-^','Color',col,'LineWidth',1,'MarkerSize',5,'MarkerEdgeColor',col)
    else
        plot(y0,x0,'-v','Color',col,'LineWidth',1,'MarkerSize',5,'MarkerEdgeColor',col)
    end
end
hold off
filename = [thename,'_intensity','.pdf'];
saveas(gcf,filename);




