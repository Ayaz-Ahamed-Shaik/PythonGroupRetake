window.addEventListener('load',()=>{
    if(window.location.pathname==="/oldcar")
    {
        fetch('/fetchcar',{headers:{'Content-type':'application/json'}})
        .then(e=>e.json())
        .then(data=>{
           const cars=data.cars;
        const container=document.querySelector('.buycarsection3');
        cars.forEach(item=>{
              const carSection=document.createElement('div');
              carSection.classList.add('CarSection');
              const image=document.createElement('img');
              const text=document.createElement('h3');
              
              image.src=`static/uploads/${item.carpic}`;
              text.innerText=`${item.brand} ${item.driven} ${item.variant} ${item.year} ${item.state}` 
              
              image.style.width="100%";
              image.style.height="100%";
              carSection.append(image);
              carSection.append(text);
              container.append(carSection);
        });
        })
        .catch(exp=>
            {console.log("Error",exp);}
        )
    }
});