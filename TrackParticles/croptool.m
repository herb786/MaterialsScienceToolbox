function [yt yb xl xr] = croptool(crop,thr)
    di0=length(crop(:,1));
    di1=length(crop(1,:));
    % Searching the left coordinate looking up to each pixel according to
    % the threshold intensity
    for b=1:di1
        for a=1:di0
            if crop(a,b)> thr
                break;
            end
            xl=b;
        end
        if crop(a,b)> thr 
            break;
        end
    end
    % the same for the right coordinate
    for b=di1:-1:1
        for a=1:di0
            if crop(a,b)> thr 
                break;
            end
            xr=b;
        end
        if crop(a,b)> thr
            break;
        end
    end
    % the same for the top coordinate
    for a=1:di0
        for b=1:di1
            if crop(a,b)> thr 
                break;
            end
            yt=a;
        end
        if crop(a,b)> thr 
            break;
        end
    end
    % the same for the bottom coordinate
    for a=di0:-1:1
        for b=1:di1
            if crop(a,b)> thr 
                break;
            end
            yb=a;
        end
        if crop(a,b)> thr 
            break;
        end
    end
end