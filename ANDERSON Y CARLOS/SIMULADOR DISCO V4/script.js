let chart=null;

function fcfs(head, req){
  let total=0,current=head;
  let path=[head];
  req.forEach(r=>{
    total+=Math.abs(current-r);
    current=r;
    path.push(r);
  });
  return {total,path};
}

function sstf(head, req){
  let pending=[...req],current=head,total=0,path=[head];
  while(pending.length){
    pending.sort((a,b)=>Math.abs(a-current)-Math.abs(b-current));
    let next=pending.shift();
    total+=Math.abs(current-next);
    current=next;
    path.push(next);
  }
  return {total,path};
}

function scan(head, req, size){
  let left=req.filter(x=>x<head).sort((a,b)=>b-a);
  let right=req.filter(x=>x>=head).sort((a,b)=>a-b);
  let path=[head,...right,size-1,...left];
  let total=0;
  for(let i=1;i<path.length;i++) total+=Math.abs(path[i]-path[i-1]);
  return {total,path};
}

function look(head, req){
  let left=req.filter(x=>x<head).sort((a,b)=>b-a);
  let right=req.filter(x=>x>=head).sort((a,b)=>a-b);
  let path=[head,...right,...left];
  let total=0;
  for(let i=1;i<path.length;i++) total+=Math.abs(path[i]-path[i-1]);
  return {total,path};
}

function runSimulation(){
  const head=parseInt(document.getElementById('head').value);
  const req=document.getElementById('requests').value.split(',').map(Number);
  const size=parseInt(document.getElementById('diskSize').value);

  const results={
    FCFS:fcfs(head,req),
    SSTF:sstf(head,req),
    SCAN:scan(head,req,size),
    LOOK:look(head,req)
  };

  const tbody=document.querySelector("#resultsTable tbody");
  tbody.innerHTML='';

  Object.entries(results).forEach(([name,res])=>{
    let avg=(res.total/(res.path.length-1)).toFixed(2);
    const seekTime = res.total * 0.1;
    const throughput = (req.length / seekTime).toFixed(3);
    const waiting = (seekTime / req.length).toFixed(2);

    tbody.innerHTML+=`
      <tr>
        <td>${name}</td>
        <td>${res.total}</td>
        <td>${avg}</td>
        <td>${seekTime.toFixed(2)}</td>
        <td>${throughput}</td>
        <td>${waiting}</td>
      </tr>`;
  });

  document.getElementById("paths").innerHTML=Object.entries(results)
    .map(([n,r])=>`<p><b>${n}</b>: ${r.path.join(" → ")}</p>`).join("");

  const labels=Object.keys(results);
  const data=labels.map(x=>results[x].total);
  if(chart) chart.destroy();
  chart=new Chart(document.getElementById('chart'),{
    type:'bar',
    data:{labels,datasets:[{label:'Distancia Total',data}]}
  });

  let best = Object.entries(results).sort((a,b)=>a[1].total-b[1].total)[0];
  document.getElementById("conclusion").innerHTML=
    `El algoritmo más eficiente para esta carga fue <b>${best[0]}</b>, ya que presentó la menor distancia recorrida (${best[1].total} cilindros).`;

  document.getElementById("interpretation").innerHTML=
    `Los resultados muestran cómo cada algoritmo organiza las solicitudes de disco. Una menor distancia recorrida generalmente implica menor tiempo de acceso y mayor eficiencia.`;
}

function randomWorkload(){
  let arr=[];
  for(let i=0;i<15;i++) arr.push(Math.floor(Math.random()*200));
  document.getElementById("requests").value=arr.join(",");
}

function runExperiment(){
  let totals={ FCFS:0, SSTF:0, SCAN:0, LOOK:0 };
  for(let i=0;i<100;i++){
    let req=[];
    for(let j=0;j<20;j++) req.push(Math.floor(Math.random()*200));
    totals.FCFS+=fcfs(53,req).total;
    totals.SSTF+=sstf(53,req).total;
    totals.SCAN+=scan(53,req,200).total;
    totals.LOOK+=look(53,req).total;
  }
  alert(`FCFS: ${(totals.FCFS/100).toFixed(2)} 
SSTF: ${(totals.SSTF/100).toFixed(2)} 
SCAN: ${(totals.SCAN/100).toFixed(2)} 
LOOK: ${(totals.LOOK/100).toFixed(2)}`);
}

runSimulation();
