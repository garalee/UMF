function [C,L,U] = SpectralClustering(W,k,Type)


degs = sum(W,2);
D = sparse(1:size(W,1),1:size(W,2),degs);

L = D-W

switch Type
    case 2
      %avoid dividing by zero
      degs(degs == 0) = eps;
      % calculate inverse of D
      D = spdiags(1./degs,0,size(D,1),size(D,2));

      L = D*L;
    case 3
      degs(degs == 0) = eps;
      D = spdiags(1./(degs.^0.5),0,size(D,1),size(D,2));

      L = D * L * D;
end

diff = eps;
[U,~] = eigs(L,k,diff);

if Type == 3
  U = bsxfun(@rdivide,U,sqrt(sum(U.^2,2)));
end

C = kmeans(U,k,'start','cluster',0,1,2,3,4,5,6,7);
C = sparse(1:size(D,1),C,1);