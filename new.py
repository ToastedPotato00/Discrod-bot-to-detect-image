import discord
import os
from discord.ext import commands
from ai import image_detection
intents = discord.Intents.default()
intents.message_content = True

SAVE_FOLDER = "saved_images"

def has_image_attachment(message):
    """
    Checks if a message contains an image attachment
    
    Parameters:
    message (discord.Message): The Discord message to check
    
    Returns:
    bool: True if the message contains an image attachment, false otherwise
    """
    # Check if the message has any attachments
    if len(message.attachments) == 0:
        return False
    
    # Array of common image file extensions
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tiff', '.svg']
    
    # Check if any attachment has an image file extension
    for attachment in message.attachments:
        attachment_name = attachment.filename.lower() if attachment.filename else ''
        
        # Check for image extension or content_type
        if any(attachment_name.endswith(ext) for ext in image_extensions) or \
           (attachment.content_type and attachment.content_type.startswith('image/')):
            return True
    
    return False


bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    try:
        # Get the directory where the script is running
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Create a path to the saved_images folder within that directory
        save_path = os.path.join(script_dir, SAVE_FOLDER)
        # Create the directory
        os.makedirs(save_path, exist_ok=True)
        print(f"Created or verified save folder: {save_path}")
    except Exception as e:
        print(f"Error creating directory: {e}")

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hi! I am a bot {bot.user}!')

@bot.command()
async def heh(ctx, count_heh = 5):
    await ctx.send("he" * count_heh)

@bot.command()
async def checkimage(ctx):
    if has_image_attachment(ctx.message):
        saved_files = []
        for attachment in ctx.message.attachments:  # Changed message to ctx.message
            attachment_name = attachment.filename.lower()
            image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tiff', '.svg']
            
            # Only save if it's an image
            if any(attachment_name.endswith(ext) for ext in image_extensions):
                try:
                    # Generate a unique filename with timestamp
                    filename = f"{attachment.filename}"
                    filepath = os.path.join(SAVE_FOLDER, filename)
                    
                    # Use attachment.save() to save the file
                    await attachment.save(filepath)
                    
                    saved_files.append(filepath)
                    print(f"Image saved to {filepath}")
                    print(f"Original URL: {attachment.url}")
                except Exception as e:
                    print(f"Error saving image: {e}")
        
        # Respond in the channel that images were saved
        if saved_files:
            check_image = image_detection(image_name=filepath)
            if check_image == "Kucing":
                await ctx.send(f"Saved {len(saved_files)} from your message!")
                await ctx.send("Kucing suka makan ikan")
            elif check_image == "Anjing":
                await ctx.send(f"Saved {len(saved_files)} from your message!")
                await ctx.send("Anjing suka bermain tulang")
            elif check_image == "Sapi":
                await ctx.send(f"Saved {len(saved_files)} from your message!")
                await ctx.send("Sapi suka memakan rumput")
            elif check_image == "Burung":
                await ctx.send(f"Saved {len(saved_files)} from your message!")
                await ctx.send("Burung suka terbang di udara")
        else:
            await ctx.send("No valid images to save.")
    else:
        await ctx.send("No image found in this message.")
        
bot.run("token")