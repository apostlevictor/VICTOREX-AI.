const TelegramBot = require('node-telegram-bot-api');

// Replace with your actual bot token from @BotFather
const BOT_TOKEN = process.env.BOT_TOKEN || 'YOUR_BOT_TOKEN';
// Replace with your personal Telegram user ID
const OWNER_ID = process.env.OWNER_ID || 'YOUR_USER_ID';

const bot = new TelegramBot(BOT_TOKEN);

// Store user information temporarily (for demo - use database in production)
const userSessions = new Map();

// Main bot handler
module.exports = async (req, res) => {
  if (req.method === 'POST') {
    try {
      const update = req.body;
      
      if (update.message) {
        const message = update.message;
        const chatId = message.chat.id;
        const text = message.text || '';
        const userName = message.from.first_name + (message.from.last_name ? ' ' + message.from.last_name : '');
        const userId = message.from.id;

        // Check if message is from owner
        if (userId.toString() === OWNER_ID.toString()) {
          await handleOwnerMessage(message);
        } else {
          // Message from user - forward to owner
          await handleUserMessage(message);
        }
      }
      
      res.status(200).json({ ok: true });
    } catch (error) {
      console.error('Error:', error);
      res.status(500).json({ error: 'Internal error' });
    }
  } else {
    res.status(200).json({ 
      status: 'Victorex Trader Bot is running',
      description: 'Privacy intermediary bot'
    });
  }
};

// Handle messages from users (forward to owner)
async function handleUserMessage(message) {
  const chatId = message.chat.id;
  const user = message.from;
  const text = message.text || '';
  
  const userInfo = `👤 From: ${user.first_name} ${user.last_name || ''}
ID: ${user.id}
Username: @${user.username || 'N/A'}`;

  try {
    // Forward original message to owner
    if (message.text) {
      await bot.sendMessage(OWNER_ID, `${userInfo}\n\n💬 Message: ${text}`);
    }
    
    // Store user session
    userSessions.set(chatId, user);
    
    // Auto-reply to user
    if (text.startsWith('/start')) {
      await bot.sendMessage(chatId, `🤝 Welcome to Victorex Trader\n\nI'm an automated assistant that connects you directly with the account manager while maintaining your privacy.\n\nYour messages are forwarded securely, and mutual contacts are not visible.\n\nJust type your message and I'll forward it immediately.`);
    } else {
      await bot.sendMessage(chatId, `✅ Message received! The Victorex Trader team will respond shortly.\n\nWe value your privacy - your contact info remains protected.`);
    }
    
  } catch (error) {
    console.error('Error handling user message:', error);
  }
}

// Handle messages from owner (forward to users)
async function handleOwnerMessage(message) {
  const text = message.text || '';
  const replyToMessage = message.reply_to_message;
  
  // Check if owner is replying to a forwarded message
  if (replyToMessage && text.startsWith('/reply')) {
    await handleOwnerReply(message);
    return;
  }
  
  // Help command for owner
  if (text === '/help') {
    await bot.sendMessage(OWNER_ID, 
      `🛠️ Owner Commands:
/reply [message] - Reply to last user
/stats - Show bot statistics
/users - List recent users`);
  }
  
  // Stats command
  if (text === '/stats') {
    await bot.sendMessage(OWNER_ID, `📊 Bot Statistics:\nActive Sessions: ${userSessions.size}`);
  }
  
  // Users list
  if (text === '/users') {
    const usersList = Array.from(userSessions.entries())
      .map(([id, user]) => `${user.first_name} (ID: ${id})`)
      .join('\n') || 'No active users';
    
    await bot.sendMessage(OWNER_ID, `👥 Recent Users:\n${usersList}`);
  }
}

// Handle owner replies to users
async function handleOwnerReply(message) {
  const text = message.text.replace('/reply', '').trim();
  const replyToMessage = message.reply_to_message;
  
  if (replyToMessage && replyToMessage.text) {
    // Extract user ID from forwarded message (you might need to parse this better)
    const lines = replyToMessage.text.split('\n');
    const idLine = lines.find(line => line.startsWith('ID: '));
    
    if (idLine) {
      const userId = idLine.replace('ID: ', '').trim();
      
      try {
        // Send message to user
        await bot.sendMessage(userId, `📨 Response from Victorex Trader:\n\n${text}`);
        await bot.sendMessage(OWNER_ID, `✅ Reply sent to user ${userId}`);
      } catch (error) {
        await bot.sendMessage(OWNER_ID, `❌ Failed to send reply. User may have blocked bot.`);
      }
    }
  }
}
