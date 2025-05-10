import logging

# Configure logging to ensure Railway prints logs correctly
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[logging.StreamHandler()]  # Ensure logs appear in Railway console
)

def start_bot():
    print("🤖 Tensai Bot Started Successfully!", flush=True)  # Flush ensures logs appear instantly
    logging.info("🤖 Tensai Rename Bot Started Successfully!")
