% Load your dataset
load('Rosettaupdated.mat');

% Create adjusted price columns for the entire dataset by dividing with CFACPR
CRSP.AdjustedPRC = CRSP.PRC ./ CRSP.CFACPR;
CRSP.AdjustedOPENPRC = CRSP.OPENPRC ./ CRSP.CFACPR;

% Replace NaNs and Infs (which might result from division by zero)
CRSP.AdjustedPRC(isnan(CRSP.AdjustedPRC) | isinf(CRSP.AdjustedPRC)) = NaN;
CRSP.AdjustedOPENPRC(isnan(CRSP.AdjustedOPENPRC) | isinf(CRSP.AdjustedOPENPRC)) = NaN;

% Rename the adjusted columns to PRC and OPENPRC
CRSP.PRC = CRSP.AdjustedPRC;
CRSP.OPENPRC = CRSP.AdjustedOPENPRC;

% Create the priceData directory if it doesn't exist
output_folder = 'priceDataRAW';
if ~exist(output_folder, 'dir')
    mkdir(output_folder);
end

% Convert the TICKER column to a cell array of character vectors if it's not already
if ~iscell(CRSP.TICKER)
    tickers = cellstr(CRSP.TICKER);
else
    tickers = CRSP.TICKER;
end

% Find all unique tickers and remove any '<undefined>' entries
unique_tickers = unique(strtrim(tickers));
unique_tickers(strcmp(unique_tickers, '<undefined>')) = [];

% Define the columns to save (now adjusted PRC and OPENPRC)
columns_to_save = {'date', 'TICKER', 'PRC', 'RET', 'OPENPRC'};

% Loop through each unique ticker
for i = 1:length(unique_tickers)
    ticker = unique_tickers(i);
    
    % Skip iteration if ticker is '<undefined>' or empty
    if strcmp(ticker, '<undefined>') || isempty(ticker)
        fprintf('Skipping invalid or undefined ticker.\n');
        continue;
    end
    
    % Print the current ticker being processed
    fprintf('Processing ticker: %s\n', ticker{1});
    
    % Filter the data for the current ticker
    ticker_data = CRSP(strcmp(tickers, ticker), :);

    % Select only the desired columns
    ticker_data = ticker_data(:, columns_to_save);
    
    % Sort the data by date in ascending order
    ticker_data = sortrows(ticker_data, 'date');

    % Check if data for this ticker is empty and print a message if it is
    if isempty(ticker_data)
        fprintf('No data for ticker: %s, skipping...\n', ticker{1});
        continue;
    end
    
    % Print the number of rows being saved for the current ticker
    fprintf('Saving %d rows for ticker: %s\n', height(ticker_data), ticker{1});

    % Define the filename for the CSV
    filename = fullfile(output_folder, strcat(ticker{1}, '.csv'));

    % Save the filtered data to a CSV file named after the ticker
    writetable(ticker_data, filename);
end

disp('All tickers have been processed and saved.');
