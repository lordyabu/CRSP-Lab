% Load your dataset
load('Rosettaupdated.mat');

% Specify the ticker you want to check
tickerToCheck = 'AHPI'; % Replace 't' with your actual ticker string

% Ensure the TICKER column is a cell array of character vectors if it's not already
if ~iscell(CRSP.TICKER)
    tickers = cellstr(CRSP.TICKER);
else
    tickers = CRSP.TICKER;
end

% Filter the data for the specific ticker
tickerData = CRSP(strcmp(tickers, tickerToCheck), :);

% Check if there is any negative value in the 'PRC' column
hasNegative = any(tickerData.PRC < 0);

% Output the result
if hasNegative
    fprintf('The ticker %s has at least one negative price.\n', tickerToCheck);
else
    fprintf('All prices for the ticker %s are non-negative.\n', tickerToCheck);
end
