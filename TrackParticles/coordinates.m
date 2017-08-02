function [x0 y0 r] = coordinates(fourier,thr)
    [d0 d1] = size(fourier);
    % threshold intensity
    d0 = int16(d0/3);
    % normalization of the matrix
    normz=abs(fourier);
    minn=min(min(normz));
	maxx=max(max(normz));
	normz=(normz-minn)/(maxx-minn);
    % Searching the left coordinate looking up to each pixel according to
    % the threshold intensity
    for b=1:d1
        for a=1:d0
            if normz(a,b)> thr
                break;
            end
            xll=b-4;
        end
        if normz(a,b)> thr 
            break;
        end
    end
    % the same for the right coordinate
    for b=d1:-1:1
        for a=1:d0
            if normz(a,b)> thr 
                break;
            end
            xrr=b+4;
        end
        if normz(a,b)> thr
            break;
        end
    end
    % the same for the top coordinate
    for a=1:d0
        for b=1:d1
            if normz(a,b)> thr 
                break;
            end
            ytt=a-4;
        end
        if normz(a,b)> thr 
            break;
        end
    end
    % Find the center in the horizontal axis and the radius
        x0 = int16((xrr+xll)/2);
        r = int16((xrr-xll)/2);
    % Searching for the bottom coordinate in a top third of total area
    for a=ytt+3*r:-1:1
        for b=1:d1
            if normz(a,b)> thr 
                break;
            end
            ybb=a+4;
        end
        if normz(a,b)> thr 
            break;
        end
    end
    % find the center inthe vertical axis
        y0 = int16((ytt+ybb)/2);       
end
 