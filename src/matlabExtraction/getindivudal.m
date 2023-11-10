% Load your dataset
load('Rosettaupdated.mat');

% Create the priceData directory if it doesn't exist
output_folder = 'priceData';
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

% Define the columns to save
columns_to_save = {'date', 'TICKER', 'PRC', 'RET', 'OPENPRC'};

% Loop through each unique ticker
for i = 1:length(unique_tickers)
    ticker = unique_tickers{i};
    
    % Skip iteration if ticker is '<undefined>' or empty
    if strcmp(ticker, '<undefined>') || isempty(ticker)
        fprintf('Skipping invalid or undefined ticker.\n');
        continue;
    end
    
    % Print the current ticker being processed
    fprintf('Processing ticker: %s\n', ticker);
    
    % Filter the data for the current ticker
    ticker_data = CRSP(strcmp(tickers, ticker), :);

    % Select only the desired columns
    ticker_data = ticker_data(:, columns_to_save);
    
    % Sort the data by date in ascending order
    ticker_data = sortrows(ticker_data, 'date');
    
    % Find the last indices where PRC, RET, or OPENPRC is NaN and remove them
    last_valid_index = find(~isnan(ticker_data.PRC) & ~isnan(ticker_data.RET) & ~isnan(ticker_data.OPENPRC), 1, 'last');
    if ~isempty(last_valid_index) && last_valid_index < height(ticker_data)
        ticker_data = ticker_data(1:last_valid_index, :);
    end

    % Check if data for this ticker is empty and print a message if it is
    if isempty(ticker_data)
        fprintf('No data for ticker: %s, skipping...\n', ticker);
        continue;
    end
    
    % Print the number of rows being saved for the current ticker
    fprintf('Saving %d rows for ticker: %s\n', height(ticker_data), ticker);

    % Define the filename for the CSV
    filename = fullfile(output_folder, strcat(ticker, '.csv'));

    % Save the filtered data to a CSV file named after the ticker
    writetable(ticker_data, filename);
end

disp('All tickers have been processed and saved.');
