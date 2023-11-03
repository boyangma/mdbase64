# mdbase64
Convert markdown files with extra images (local or web images) to single base64-embedded markdown files

# Introduction
Although markdown is a convenient text format, it has some aspects I don't like, especially handling images.

As you know, markdown can insert an image by referencing its local path or URL.

However, the image is possible to result in invalid if the '.md' file and the image source file are not moving together or the URL becomes invalid.

Obviously, it is a terrible disaster if you use the markdown as your notebook format. 

Fortunately, we can embed an image to the '.md' file by converting it to base64 string.

Although the size of the '.md' file will be huge than normal markdown files, it is worth to do this for your note data safety.

On the other hand, there is not any bottleneck of performance for today's computer to open a large markdown file. 

So, I write a useful Python script to convert your markdown file(s) to image-embedded version.

**The script supports converting both local and web images in the markdown files.**

# Usage
You just need to run `mdbase64.py` on Windows or Linux with two parameters, i.e., `work path` and `output path`.

**Note:** Don't forget the double quotation marks.

## Example
markdown files location: D:\notebook

output location: D:\output

```
> python mdbase64.py "D:\notebook" "D:\output"
```

The converted markdown files will be created in `D:\output`

<br>
<br>
Enjoy it!
