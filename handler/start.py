import logging

# Configure logging for Railway
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[logging.StreamHandler()]  # Ensures logs appear in Railway console
)

def start_bot():
    """Initializes Tensai Rename Bot and logs startup details."""
    print("🤖 Tensai Bot Started Successfully!", flush=True)  # Flush ensures Railway prints instantly
    logging.info("🤖 Tensai Rename Bot Started Successfully!")
