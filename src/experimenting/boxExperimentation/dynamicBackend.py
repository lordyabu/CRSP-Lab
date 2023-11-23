from IPython.display import display, Javascript

def setup_js_callback():
    js = """
    <script>
    var plotElement = document.getElementById('YOUR_PLOT_ID'); // Replace with your actual Plotly plot ID
    plotElement.on('plotly_relayout', function(eventData) {
        var update = {};
        if(eventData['xaxis.range[0]'] && eventData['xaxis.range[1]']) {
            var xRangeStart = new Date(eventData['xaxis.range[0]']);
            var xRangeEnd = new Date(eventData['xaxis.range[1]']);

            // Assuming you have a function to calculate y-axis range based on x-axis range
            var newYAxisRange = calculateYAxisRange(xRangeStart, xRangeEnd);

            update['yaxis.range'] = [newYAxisRange[0], newYAxisRange[1]];
            Plotly.relayout(plotElement, update);
        }
    });

    function calculateYAxisRange(xStart, xEnd) {
        // Placeholder for your logic to calculate the new y-axis range based on xStart and xEnd
        // You might need to access your data source here to determine the appropriate y-axis range
        // For example, find the min and max of the data within the xStart and xEnd range
        return [newYMin, newYMax]; // Replace with the calculated min and max for y-axis
    }
    </script>
    """
    display(Javascript(js))

# Call this function after displaying your Plotly plot in a Jupyter Notebook
setup_js_callback()
