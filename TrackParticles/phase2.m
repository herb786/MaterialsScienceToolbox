function [im,phase] = phase2(pat,thr)

% Size of pattern
[sy,sx]=size(pat);
% Matrix of zeros
D4=zeros(size(pat));
% Fourier transform of the pattern
D1=fft2(pat);
D5=ones(size(pat));
clear xnew;
% Swapping of quadrants
D2=fftshift(D1);
clear D1;
D3=D2;
clear D2;
% Filter for FFT after swapping
[x0 y0 r] = coordinates(D3(:,:),thr);
for j=1:sx
    for k=1:sy
        if (j-x0)^2+(k-y0)^2 > r^2
            D5(k,j) = 0;
        end
    end
end
D3 =  D5.*D3;
clear D5;
% Inverse FFT
im=ifft2(fftshift(D3));
% Whatever
D4(y0,x0)=D3(y0,x0);
clear D3;
% Phase computation
phase=angle(im./ifft2(fftshift(D4)));
% Take the module
im=abs(im);
clear D4;
end