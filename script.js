
document.addEventListener("DOMContentLoaded", function () {
  const fetchButton = document.getElementById("fetchButton");
  const stockSymbolInput = document.getElementById("stockSymbol");
  const stockChart = document.getElementById("stockChart");

  fetchButton.addEventListener("click", function () {
    const symbol = stockSymbolInput.value;
    if (symbol.trim() === "") {
      alert("Please enter a valid stock symbol.");
      return;
    }

    const api_key = "YOUR_ALPHAVANTAGE_API_KEY"; // Replace with your actual API key

    // Fetch stock data using the Alpha Vantage API
    const apiUrl = `https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=${symbol}&apikey=${api_key}&outputsize=full&datatype=json`;

    fetch(apiUrl)
      .then((response) => response.json())
      .then((data) => {
        const dates = Object.keys(data["Time Series (Daily)"]).reverse();
        const closingPrices = dates.map(
          (date) => parseFloat(data["Time Series (Daily)"][date]["4. close"])
        );

        // Create and update the chart
        const ctx = stockChart.getContext("2d");
        new Chart(ctx, {
          type: "line",
          data: {
            labels: dates,
            datasets: [
              {
                label: "Closing Prices",
                data: closingPrices,
                backgroundColor: "rgba(0, 123, 255, 0.1)",
                borderColor: "#007bff",
                borderWidth: 1,
              },
            ],
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
          },
        });
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  });
});

