# This Script can hide Images in other Images you only need the x and y size of the hidden image to recover it
# make sure the image you want to hide is a lot smaller than the image you hide it in, otherwise you wont have the
# full hidden image saved in the big one
# In case of problems contact me on Discord: 𝕱𝖔𝖗𝖊𝖘𝖙_𝕮𝖆𝖙#8895


from rich.console import Console
from time import sleep
from PIL import Image
import os

console = Console()


# Reads Image and Returns it as Byte String
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

# Takes an Image and a Byte String and writes the Byte String to the Image and Returns the new Image
def stegoImage(origImage: Image, origPixels, hideImage: str, hideImageSize: tuple):
    counter = 0
    hideImageSize = "".join([f"{size:016b}" for size in hideImageSize])
    for x in range(origImage.size[0]):
        for y in range(origImage.size[1]):
            for i,color in enumerate(origPixels[x,y]):
                tupleAsList = list(origPixels[x,y])
                if counter < 32:
                    if int(hideImageSize[counter]) == 0:
                        if origPixels[x,y][i] % 2 == 0:
                            pass
                        else:
                            tupleAsList[i] -= 1
                    if int(hideImageSize[counter]) == 1:
                        if origPixels[x,y][i] % 2 == 1:
                            pass
                        else:
                            tupleAsList[i] += 1
                    counter += 1
                else:
                    if counter < len(hideImage)+32:
                        if int(hideImage[counter-32]) == 0:
                            if origPixels[x,y][i] % 2 == 0:
                                pass
                            else:
                                tupleAsList[i] -= 1
                        if int(hideImage[counter-32]) == 1:
                            if origPixels[x,y][i] % 2 == 1:
                                pass
                            else:
                                tupleAsList[i] += 1
                        counter+=1
                origPixels[x,y] = tuple(tupleAsList)
    return origPixels

# get the size of the hidden image
def getHiddenImageSize(encodedImage: Image):
    encodedImagePixels = encodedImage.load()
    sizeX, sizeY = '',''
    counter = 0
    for x in range(encodedImage.size[0]):
        for y in range(encodedImage.size[1]):
            for color in encodedImagePixels[x,y]:
                if counter < 16:
                    sizeX += str(color % 2)
                    counter += 1
                elif counter < 32:
                    sizeY += str(color % 2)
                    counter += 1
    return (int(sizeX, 2), int(sizeY, 2))


# Takes the Encoded Image and a new empty Image and the hidden Image Size and Returns the decoded Image as Pixel Matrix
def decodeImage(encodedImage: Image, newImagePixels, size: tuple):
    encodedImagePixels = encodedImage.load()
    decodedImageString = ""
    decodedImageArray = []
    counter = 0                
    sizeMultiplied = size[0] * size[1] * 4 * 8 + 32 # 4 colors RGBA * 8 bits per color 
    for x in range(encodedImage.size[0]):
        for y in range(encodedImage.size[1]):
            for color in encodedImagePixels[x,y]:
                if counter < sizeMultiplied:
                    decodedImageString += str(color % 2)
                counter+=1

    tmparrray = []
    for entry in decodedImageString[32:]:
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

# Checks the Size of both images and returns if the hide image is small enough and fits in the medium image
def checkSize(origImageSize: tuple, hideImageSize: tuple):
    return False if origImageSize[0] * origImageSize[1] * 4 < hideImageSize[0] * hideImageSize[1] * 4 * 8 + 32 else True

if __name__ == "__main__":
    ACTION = input("Encode or decode? (e/d): ")

    if ACTION.lower() == "e":
        os.chdir(os.path.dirname(__file__))
        print("\n##################### Encoding enabled #####################\n")
        bigImagePath = input("Enter the file path of the image you want to use as medium: ")
        smallImagePath = input("Enter the file path of the image you want to hide (it has to be a lot smaller than the previous Image): ")
        
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

            if not checkSize(origImageSize=bigImage.size, hideImageSize=smallImage.size):
                console.log(f"[red]The Image you want to hide is not small enough or the medium Image is to small.\nProceeding can result in the image being only half visible or the Programm crashing... [/red]")
                ans = input("Do you want to continue? (y/N): ")
                if ans.lower() == "y":
                    console.log(f"[green]Proceeding...[/green]")
                else:
                    console.log(f"[red]Aborting...[/red]")
                    exit()

            bigImagePixels = stegoImage(origImage=bigImage, origPixels=bigImagePixels, hideImage=smallImageString, hideImageSize=smallImage.size)

            bigImage.save('EncodedHiddenImage.png')
            console.log(f"[green]Saved Image as:[/green] [yellow]EncodedHiddenImage.png[/yellow]")
            console.log(f'[bold][red]Done!')
    elif ACTION.lower() == "d":
        os.chdir(os.path.dirname(__file__))
        
        print("\n##################### Decoding enabled #####################\n")
        
        encodedImagePath = input("Enter the file path of the image you want to decode: ")
            
        with console.status("[bold green]Decoding Image...") as status:
            encodedImage = Image.open(encodedImagePath)
            console.log(f"[green]Opened Encoded Image[/green]")
            encodedImage = encodedImage.convert('RGBA')
            console.log(f"[green]Converted from[/green] [yellow]RGB[/yellow] [green]to[/green] [violet]RGBA[/violet]")
            
            hiddenImageSize = getHiddenImageSize(encodedImage)
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
