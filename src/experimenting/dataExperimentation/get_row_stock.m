% Load your dataset
load('Rosettaupdated.mat');  % Replace with the actual name of your .mat file that contains the CRSP variable

% Define the ticker and date you want to check
tickerToCheck = 'AAPL';  % The ticker to check
dateToCheck = 20201231;  % The date to check in YYYYMMDD format

% Ensure the TICKER column is a cell array of character vectors if it's not already
if ~iscell(CRSP.TICKER)
    tickers = cellstr(CRSP.TICKER);
else
    tickers = CRSP.TICKER;
end

% Convert the date column to the correct format if it's not already
% This assumes the date is stored in a column named 'date' in the CRSP table
% If the column is named differently, adjust 'date' to the correct column name
if ~isnumeric(CRSP.date)  % Replace this line with the actual date column name
    dates = datenum(CRSP.date, 'YYYYMMDD');  % Convert to numeric format if necessary
else
    dates = CRSP.date;
end

% Filter the data for the specific ticker and date
tickerData = CRSP(strcmp(tickers, tickerToCheck) & dates == dateToCheck, :);

% Check if any data was found for that ticker and date
if isempty(tickerData)
    fprintf('No data found for ticker %s on date %d.\n', tickerToCheck, dateToCheck);
else
    % Display the row for the ticker on the specific date
    disp(tickerData);
end
