% Load your dataset
load('Rosettaupdated.mat');

% Create adjusted price columns for the entire dataset by dividing with CFACPR
% We use ./ to perform element-wise division
CRSP.AdjustedPRC = CRSP.PRC ./ CRSP.CFACPR;
CRSP.AdjustedOPENPRC = CRSP.OPENPRC ./ CRSP.CFACPR;

% Replace NaNs and Infs (which might result from division by zero)
CRSP.AdjustedPRC(isnan(CRSP.AdjustedPRC) | isinf(CRSP.AdjustedPRC)) = CRSP.PRC(isnan(CRSP.AdjustedPRC) | isinf(CRSP.AdjustedPRC));
CRSP.AdjustedOPENPRC(isnan(CRSP.AdjustedOPENPRC) | isinf(CRSP.AdjustedOPENPRC)) = CRSP.OPENPRC(isnan(CRSP.AdjustedOPENPRC) | isinf(CRSP.AdjustedOPENPRC));

% Display a random sample of 25 rows from the adjusted dataset
sampleRows = datasample(CRSP, 25, 'Replace', false);
disp('Random sample of 25 rows from the adjusted dataset:');
disp(sampleRows(:, {'TICKER', 'date', 'PRC', 'OPENPRC', 'CFACPR', 'AdjustedPRC', 'AdjustedOPENPRC'}));

save('RosettaupdatedAdj.mat', 'CRSP');

% Display a confirmation message
disp('The adjusted dataset has been saved as RosettaupdatedAdj.mat');