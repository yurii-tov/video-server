function play(x)
{
    document.getElementById("video").src = '/video/' + x;
    document.getElementById("video").autoplay = true;
    document.getElementById("description").innerHTML = x;
}

function render_playlist()
{
    document.getElementById("playlist").remove();
    let playlist = document.createElement("ul");
    playlist.id = "playlist";
    // Shuffle list of videos
    for (let i = 0; i < videos.length; i++) {
        let j = Math.floor(Math.random() * videos.length);
        let a = videos[i];
        let b = videos[j];
        videos[i] = b;
        videos[j] = a;
    }
    for (let v of videos.slice(0,5)) {
        let li = document.createElement('li');
        let video = document.createElement('img');
        let text = document.createElement('pre');
        video.src = '/static/videos/' + v + '.gif';
        text.innerHTML = v;
        li.onclick = function() {
            play(v)
            render_playlist();
        };
        li.appendChild(text);
        li.appendChild(video);
        playlist.appendChild(li);
    }
    document.getElementById("player").appendChild(playlist);
}

render_playlist();
play(videos[0])
