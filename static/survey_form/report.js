function createCharts(purposeData, visitorStatusData, firstTimeVisitingData) {
    // const ctx = document.getElementById('myChart').getContext('2d');
    // Get the canvas elements from the HTML
    const purposeCanvas = document.getElementById('purposeChart');
    const visitorStatusCanvas = document.getElementById('visitorStatusChart');
    const firstTimeVisitingCanvas = document.getElementById('firstTimeVisitingChart');
  
    // Create a bar chart for Purpose of Visit
    const purposeChart = new Chart(purposeCanvas, {
      type: 'bar',
      data: {
        labels: ['Admission', 'Events', 'Others'],
        datasets: [{
          label: 'Purpose of Visit',
          data: purposeData,
          backgroundColor: ['#FFC107', '#3F51B5', '#8BC34A']
        }]
      },
      options: {
        responsive: false,
        maintainAspectRatio: true
      }
    });

  
    // Create a pie chart for Visitor Status
    const visitorStatusChart = new Chart(visitorStatusCanvas, {
      type: 'pie',
      data: {
        labels: ['Student', 'Parent', 'Other College Student'],
        datasets: [{
          label: 'Visitor Status',
          data: visitorStatusData,
          backgroundColor: ['#3F51B5', '#FFC107', '#8BC34A']
        }]
      },
      options: {
        responsive: false,
        maintainAspectRatio: true
      }
    });
  
    // Create a doughnut chart for First Time Visiting
    const firstTimeVisitingChart = new Chart(firstTimeVisitingCanvas, {
      type: 'doughnut',
      data: {
        labels: ['Yes', 'No'],
        datasets: [{
          label: 'First Time Visiting',
          data: firstTimeVisitingData,
          backgroundColor: ['#8BC34A', '#FFC107']
        }]
      },
      options: {
        responsive: false,
        maintainAspectRatio: true
      }
    });
  }

  fetch('/reports')
  .then(response => response.json())
  .then(data => {
      console.log(data)
    const purposeData = Object.values(data.purpose);
    const visitorStatusData = Object.values(data.visitor_status);
    const firstTimeVisitingData = Object.values(data.first_time_visiting);
    
    // call a function to create charts with above data
    createCharts(purposeData, visitorStatusData, firstTimeVisitingData);
  })
  .catch(error => console.error(error));

  