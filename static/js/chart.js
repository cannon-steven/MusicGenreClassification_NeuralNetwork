// The following script takes the user data in an array format and uses it to construct a donught chart.
// This is dummy data, but work on a script to generate this data is currently being written.
// Makes the chart using the result object

if (typeof(songs) == Object){
    console.log("It's in the right format");
}else{
    console.log("Turning into an object.");
    let objectSongs = turnIntoObject(songs);
    makeArray(objectSongs);
}

function turnIntoObject(objectSongs){
    return JSON.parse(objectSongs);
}

function makeArray(objectArr){
    objectArr.forEach(element => {
        let genreValues = Object.values(element.genre);
        makeChart(element, genreValues);
    });
    
}
function makeChart(song, arrayIndex){
    // this is going to be the value 'genres

    const data = {
        labels: [
            "blues", "classical", "country",
            "disco", "hiphop", "jazz",
            "metal","pop", "reggae",
            "rock"
        ],
        datasets: [{
            label: 'My First Dataset',
            data: arrayIndex,
            backgroundColor: [
            'blue',
            'grey',
            'yellow',
            'pink',
            'red',
            'purple',
            'maroon',
            'orange',
            'green',
            'black'
            ],
            hoverOffset: 10
        }]
        };
        
        const config = {
        type: 'doughnut',
        data: data,
    };

    // canvas graph 
    const housingDiv = document.getElementById(`${song.filename}_chart`);
    const canvas = document.createElement('canvas');
    canvas.setAttribute('id', `${song.filename}_chart`);
  

    // chart header
    const header2 = document.createElement('h2');
    header2.textContent = `Doughnut chart for ${song.filename}`;
    housingDiv.appendChild(header2);
    housingDiv.appendChild(canvas);

    // chart figure caption
    const figureDescription = document.createElement('dd');
    figureDescription.innerHTML = `<b>Figure 1:</b> The following chart gives a breakdown of what our Neural Network Model thinks are the most likely genres. ${song.filename} having the highest probability.`;
    housingDiv.appendChild(figureDescription);
    
    // make the chart and pass the canvas and config
    const myChart = new Chart(canvas, config);

}