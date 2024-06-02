document.getElementById('eventForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData(this);
    const date = formData.get('date');
    const month = formData.get('month');
    const cityElement = document.getElementById('city');
    const city = cityElement.options[cityElement.selectedIndex].value;
    const cityId = cityElement.options[cityElement.selectedIndex].getAttribute('data-id');

    const data = {
        date: date,
        month: month,
        city: city,
        cityId: cityId
    };
    let loader = document.getElementById("loader");
    loader.style.display="block";
    fetch('/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        console.log(data, typeof data);
        document.getElementById('output').textContent = data.message;
        loader.style.display="none";
    })
    .catch(error => {
        loader.style.display="none";
        alert("Unable to extract !")
        console.error('Error:', error)});
});