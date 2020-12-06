:: Create File List
echo file file1.mp4 >  mylist.txt 
echo file file2.mp4 >> mylist.txt
echo file file3.mp4 >> mylist.txt

:: Concatenate Files
ffmpeg -f concat -i mylist.txt -c:v copy -c:a copy merged.mp4