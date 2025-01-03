from telegram import Bot
from telegram.error import TelegramError
from .exceptions import TelenotifError
import asyncio
from functools import wraps
import logging
import sys

logger = logging.getLogger(__name__)

def _ensure_async_loop():
    """Ensure there's an event loop running that works in all environments."""
    try:
        # Try to detect if we're in IPython/Jupyter environment
        import IPython
        ipython = IPython.get_ipython()
        if ipython is not None and 'IPKernelApp' in ipython.config:
            import nest_asyncio
            nest_asyncio.apply()
    except ImportError:
        pass  # Not in IPython/Jupyter environment

    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop

class notif:
    """
    A simple notification class that sends messages via Telegram bot.
    
    Args:
        bot_token (str): Telegram bot token obtained from BotFather
        user_id (str): Telegram user ID to send notifications to
        disable_notification (bool, optional): If True, sends messages silently. Defaults to False.
    """
    
    def __init__(self, bot_token, user_id, disable_notification=False):
        # Add nest-asyncio to dependencies during initialization
        self._setup_environment()
        self.bot = Bot(token=bot_token)
        self.user_id = user_id
        self.disable_notification = disable_notification
        self._validate_credentials()
    
    def _setup_environment(self):
        """Setup the environment for async operations."""
        try:
            import nest_asyncio
        except ImportError:
            import subprocess
            import sys
            subprocess.check_call([sys.executable, "-m", "pip", "install", "nest_asyncio"])
            import nest_asyncio
        
        try:
            import IPython
            if IPython.get_ipython() is not None:
                nest_asyncio.apply()
        except ImportError:
            pass
    
    def _validate_credentials(self):
        """Validate the bot token and user ID."""
        loop = _ensure_async_loop()
        try:
            loop.run_until_complete(self.bot.get_me())
        except TelegramError as e:
            raise TelenotifError(f"Invalid bot token: {str(e)}")
    
    async def _send_message_async(self, message):
        """Send message asynchronously."""
        try:
            await self.bot.send_message(
                chat_id=self.user_id,
                text=message,
                disable_notification=self.disable_notification
            )
            return True
        except TelegramError as e:
            logger.error(f"Failed to send message: {str(e)}")
            return False

    def alert(self, message):
        """
        Send a notification message.
        
        Args:
            message (str): Message to send
            
        Returns:
            bool: True if message was sent successfully, False otherwise
        """
        loop = _ensure_async_loop()
        return loop.run_until_complete(self._send_message_async(message))
    
    def __call__(self, message):
        """Allow the notifier to be called directly."""
        return self.alert(message)
    
    def decorator(self, message=None):
        """
        Decorator to send notification after function execution.
        
        Args:
            message (str, optional): Custom message to send. If None, sends function name.
            
        Returns:
            function: Decorated function that sends notification after execution
            
        Example:
            @notifier.decorator("Task completed!")
            def long_running_task():
                # ... do something ...
                pass
        """
        def decorator_wrapper(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                result = func(*args, **kwargs)
                notification_message = message or f"Function {func.__name__} finished execution"
                self.alert(notification_message)
                return result
            return wrapper
        return decorator_wrapper