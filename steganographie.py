# This Script can hide Images in other Images you only need the x and y size of the hidden image to recover it
# make sure the image you want to hide is a lot smaller than the image you hide it in, otherwise you wont have the
# full hidden image saved in the big one
# In case of problems contact me on Discord: 𝕱𝖔𝖗𝖊𝖘𝖙_𝕮𝖆𝖙#8895


from rich.console import Console
from time import sleep
from PIL import Image
import os

console = Console()

def readImage(image: Image):
    pixels = image.load()
    colors = []
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            for color in pixels[x,y]:
                colors.append(color)
    colors = [f"{x:08b}" for x in colors]
    colors = "".join(colors)
    return colors

def stegoImage(origImage: Image, origPixels, hideImage: str):
    counter = 0
    for x in range(origImage.size[0]):
        for y in range(origImage.size[1]):
            for i,color in enumerate(origPixels[x,y]):
                tupleAsList = list(origPixels[x,y])
                if counter < len(hideImage):
                    if int(hideImage[counter]) == 0:
                        if origPixels[x,y][i] % 2 == 0:
                            pass
                        else:
                            tupleAsList[i] -= 1
                    if int(hideImage[counter]) == 1:
                        if origPixels[x,y][i] % 2 == 1:
                            pass
                        else:
                            tupleAsList[i] += 1
                    counter+=1
                    origPixels[x,y] = tuple(tupleAsList)
    return origPixels

def decodeImage(encodedImage: Image, newImagePixels, size: tuple):
    encodedImagePixels = encodedImage.load()
    decodedImageString = ""
    decodedImageArray = []
    counter = 0
    sizeMultiplied = size[0] * size[1] * 4 * 8 # 4 colors RGBA * 8 bits per color
    for x in range(encodedImage.size[0]):
        for y in range(encodedImage.size[1]):
            for color in encodedImagePixels[x,y]:
                if counter < sizeMultiplied:
                    decodedImageString += str(color % 2)
                    counter+=1
    tmparrray = []
    for entry in decodedImageString:
        tmparrray.append(entry)
        if len(tmparrray) == 8:
            tmparrray = "".join(tmparrray)
            decodedImageArray.append(int(tmparrray, 2))
            tmparrray = []
    
    counter = 0
    for x in range(size[0]):
        for y in range(size[1]):
            tupleAsList = list(newImagePixels[x,y])
            for i, color in enumerate(tupleAsList):
                if counter < len(decodedImageArray):
                    tupleAsList[i] = decodedImageArray[counter]
                    counter +=1
            newImagePixels[x,y] = tuple(tupleAsList)    
    return newImagePixels


if __name__ == "__main__":
    ACTION = input("Encode or decode? (e/d): ")

    if ACTION.lower() == "e":
        os.chdir(os.path.dirname(__file__))
        print("\n##################### Encoding enabled #####################")
        bigImagePath = input("Enter the file path of the image you want to use as medium: ")
        smallImagePath = input("Enter the file path of the image you want to hide (it has to be smaller than the previous Image): ")
        
        with console.status("[bold yellow]Encoding Image...") as status:
            bigImage = Image.open(bigImagePath)
            smallImage = Image.open(smallImagePath)
            console.log(f"[green]Opened Images[/green]")
            
            bigImage = bigImage.convert('RGBA')
            smallImage = smallImage.convert('RGBA')
            console.log(f"[green]Converted Images from[/green] [yellow]RGB[/yellow] [green]to[/green] [violet]RGBA[/violet]")

            smallImageString = readImage(smallImage)
            bigImagePixels = bigImage.load()
            console.log(f"[green]Reading Images[/green]")

            bigImagePixels = stegoImage(origImage=bigImage, origPixels=bigImagePixels, hideImage=smallImageString)

            bigImage.save('EncodedHiddenImage.png')
            console.log(f"[green]Saved Image as:[/green] [yellow]EncodedHiddenImage.png[/yellow]")
            console.log(f'[bold][red]Done!')
    elif ACTION.lower() == "d":
        os.chdir(os.path.dirname(__file__))
        
        print("\n##################### Decoding enabled #####################")
        
        encodedImagePath = input("Enter the file path of the image you want to decode: ")
        hiddenImageSizeX = int(input("Enter the [X] size of the hidden image: "))
        hiddenImageSizeY = int(input("Enter the [Y] size of the hidden image: "))
        hiddenImageSize = (hiddenImageSizeX, hiddenImageSizeY)
            
        with console.status("[bold green]Decoding Image...") as status:
            encodedImage = Image.open(encodedImagePath)
            console.log(f"[green]Opened Encoded Image[/green]")
            encodedImage = encodedImage.convert('RGBA')
            console.log(f"[green]Converted from[/green] [yellow]RGB[/yellow] [green]to[/green] [violet]RGBA[/violet]")

            decoded = Image.new("RGBA", hiddenImageSize)
            console.log(f"[green]Created new empty Image[/green]")
            decodedpix = decoded.load()
            decodedpix = decodeImage(encodedImage, decodedpix, hiddenImageSize)
            console.log(f"[green]Decoded Image[/green]")
            decoded.save("DecodedHiddenImage.png")
            console.log(f"[green]Saved Image as:[/green] [yellow]DecodedHiddenImage.png[/yellow]")
            console.log(f'[bold][red]Done!')
            decoded.show()

    else:
        print("Please enter either 'e' or 'd'")
