% Load the dataset from the MAT-file
loadedData = load('Rosettaupdated.mat');

% Access the 'CRSP' table in the loaded data
CRSP = loadedData.CRSP;

% Convert 'TICKER' to a cell array of character strings, if it's not already
if ~iscellstr(CRSP.TICKER)
    CRSP.TICKER = cellstr(CRSP.TICKER);
end

% Trim whitespace from the 'TICKER' column
CRSP.TICKER = strtrim(CRSP.TICKER);

% Filter to include only those rows where both FACPR and CFACPR have values and TICKER is 'AAPL'
rowsWithFacprAndCfacprForAapl = CRSP(~isnan(CRSP.FACPR) & CRSP.FACPR ~= 0 & ...
                                     ~isnan(CRSP.CFACPR) & CRSP.CFACPR ~= 0 & ...
                                     strcmp(CRSP.TICKER, 'AAPL'), :);

% Display a random sample of rows (up to 100)
numRowsToSample = min(height(rowsWithFacprAndCfacprForAapl), 100);
sampleRows = datasample(rowsWithFacprAndCfacprForAapl, numRowsToSample, 'Replace', false);

disp('Random sample of rows with FACPR and CFACPR values for TICKER AAPL:');
disp(sampleRows);
