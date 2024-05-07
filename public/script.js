document.addEventListener('DOMContentLoaded', function () {
  const loginForm = document.querySelector('.login100-form');
  
  // Add event listener for form submission
  loginForm.addEventListener('submit', async function (event) {
    event.preventDefault(); // Prevent default form submission
    
    // Get username and password input values
    const username = document.querySelector('input[name="Username"]').value;
    const password = document.querySelector('input[name="pass"]').value;
    
    // Perform validation
    if (username === 'admin' && password === 'admin10') {
      try {
        const response = await fetch('/fetchData', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json'
          },
        });
        
        if (response.ok) {
          const data = await response.json();
          displayData(data);
        } else {
          console.error('Error fetching data:', response.statusText);
        }
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    } else {
      alert('Invalid username or password');
    }
  });
  
  function displayData(data) {
    const container = document.querySelector('.container-login100');
    container.innerHTML = ''; // Clear previous content
    
    // Create table element
    const table = document.createElement('table');
    table.classList.add('data-table');
    
    // Create table header row
    const headerRow = document.createElement('tr');
    const headers = ['ImagePath', 'DetectedObjects', 'fromDist', 'Measurements'];
    headers.forEach(headerText => {
      const th = document.createElement('th');
      th.textContent = headerText;
      headerRow.appendChild(th);
    });
    table.appendChild(headerRow);
    
    // Populate table with data
    data.forEach(item => {
      const row = document.createElement('tr');
      Object.values(item).forEach(value => {
        const cell = document.createElement('td');
        cell.textContent = value;
        row.appendChild(cell);
      });
      table.appendChild(row);
    });
    
    container.appendChild(table);
  }
  
});
