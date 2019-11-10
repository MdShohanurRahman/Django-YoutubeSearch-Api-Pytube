from pytube import YouTube

YouTube('https://www.youtube.com/watch?v=7CVtTOpgSyY').streams.first().download()
