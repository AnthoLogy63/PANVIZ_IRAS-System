'use strict';
document.addEventListener('DOMContentLoaded', () => {
  const element = document.getElementById('chart-data');
  if (!element) return;
  if (!window.Chart) {
    document.querySelectorAll('.chart-frame').forEach(frame => {
      frame.hidden = true;
      const detail = frame.parentElement.querySelector('details');
      if (detail) detail.open = true;
    });
    return;
  }
  const data = JSON.parse(element.textContent);
  const colors = ['#119d90','#437ab7','#8d79b7','#d6a250','#64b6b2','#b57b92'];
  Chart.defaults.font.family = 'Segoe UI, system-ui, sans-serif';
  Chart.defaults.color = '#718394';
  const weekly = document.getElementById('weekly-chart');
  new Chart(weekly, {
    type:'line',
    data:{labels:Object.keys(data.weeks),datasets:[{label:'Notificaciones IRAS',data:Object.values(data.weeks),borderColor:colors[0],backgroundColor:'rgba(17,157,144,.09)',fill:true,borderWidth:3,tension:.3,pointRadius:4,pointHoverRadius:7,pointBackgroundColor:'#fff',pointBorderWidth:2}]},
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{y:{beginAtZero:true,ticks:{precision:0},border:{display:false},grid:{color:'#edf1f5'}},x:{grid:{display:false},border:{display:false}}},interaction:{intersect:false,mode:'index'}}
  });
  new Chart(document.getElementById('district-chart'), {
    type:'doughnut',data:{labels:Object.keys(data.districts),datasets:[{data:Object.values(data.districts),backgroundColor:colors,borderWidth:5,borderColor:'#fff',hoverOffset:5}]},
    options:{responsive:true,maintainAspectRatio:false,cutout:'76%',plugins:{legend:{display:false},tooltip:{callbacks:{label:context=>context.label+': '+context.raw+' notificaciones'}}}}
  });
});
