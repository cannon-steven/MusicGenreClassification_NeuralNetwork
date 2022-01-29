function uploadFile(){
    document.getElementById("upload").click()
}


function parseFileName(str){
    return str.slice(0, -3) // Assumes string is of format "filename_li"
}


function getMax(jsonArr){
    let max;
    for (element in jsonArr){
        if (max == null || parseInt(jsonArr[element]) > parseInt(jsonArr[max])){
            max = element
        }
    }
    return max
}


function showResults(fileName, resultPages){
    // Hide all results pages
    for (page of resultPages){
        page.style.display = "none"
    }
    // Hide "none selected" page
    document.getElementById("noSelection").style.display = "none"
    // Reveal selected results page
    document.getElementById(fileName + "_results").style.display = "flex"
}

// Get arrays of DOM elements
var songList = document.getElementsByClassName("songList")
var resultPages = document.getElementsByClassName("results")

// Add event listeners to the song list to display results when clicked
for (song of songList){
    let fileName = parseFileName(song.id)
    song.onclick = function(){showResults(fileName, resultPages)}
}



// function updateSongList(){
//     fetch
// }