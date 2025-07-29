<template>
  <div class="chat-container">
    <div class="card">
      <div class="card-header bg-primary text-white d-flex justify-content-between align-items-center">
        <span>Chat App</span>
        <span class="badge bg-light text-dark">{{ onlineUsers }} online</span>
      </div>
      
      <div class="card-body chat-messages" ref="messagesContainer">
        <div v-for="(message, index) in messages" :key="index" 
             class="message mb-2 d-flex"
             :class="{'justify-content-end': message.sender === 'me', 'justify-content-start': message.sender !== 'me'}">
          <div class="message-bubble" 
               :class="{'bg-primary text-white': message.sender === 'me', 'bg-light': message.sender !== 'me'}">
            <div class="message-sender small">{{ message.sender }}</div>
            <div class="message-text">{{ message.text }}</div>
            <div class="message-time small text-muted">{{ message.time }}</div>
          </div>
        </div>
      </div>
      
      <div class="card-footer">
        <form @submit.prevent="sendMessage" class="d-flex">
          <input v-model="newMessage" 
                 type="text" 
                 class="form-control me-2" 
                 placeholder="Type your message..." 
                 required>
          <button type="submit" class="btn btn-success">
            <i class="bi bi-send"></i> Send
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ChatComponent',
  data() {
    return {
      messages: [
        { sender: 'bot', text: 'Hello! How can I help you today?', time: '10:00 AM' },
        { sender: 'me', text: 'Hi there! I need some assistance.', time: '10:02 AM' },
        { sender: 'bot', text: 'Sure, what do you need help with?', time: '10:02 AM' }
      ],
      newMessage: '',
      onlineUsers: 1
    }
  },
  methods: {
    sendMessage() {
      if (this.newMessage.trim() === '') return;
      
      // Add user message
      this.messages.push({
        sender: 'me',
        text: this.newMessage,
        time: this.getCurrentTime()
      });
      
      // Simulate bot response after 1 second
      setTimeout(() => {
        this.messages.push({
          sender: 'bot',
          text: this.generateResponse(),
          time: this.getCurrentTime()
        });
        this.scrollToBottom();
      }, 1000);
      
      this.newMessage = '';
      this.scrollToBottom();
    },
    getCurrentTime() {
      const now = new Date();
      return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    },
    generateResponse() {
      const responses = [
        "I understand. Can you tell me more?",
        "Thanks for sharing that information.",
        "Let me check that for you.",
        "Interesting point! What else would you like to know?",
        "I'll help you with that."
      ];
      return responses[Math.floor(Math.random() * responses.length)];
    },
    scrollToBottom() {
      this.$nextTick(() => {
        const container = this.$refs.messagesContainer;
        container.scrollTop = container.scrollHeight;
      });
    }
  },
  mounted() {
    this.scrollToBottom();
  }
}
</script>

<style scoped>
.chat-container {
  max-width: 500px;
  margin: 0 auto;
}

.chat-messages {
  height: 300px;
  overflow-y: auto;
  padding: 10px;
}

.message-bubble {
  max-width: 70%;
  padding: 8px 12px;
  border-radius: 18px;
  margin-bottom: 4px;
}

.message-sender {
  font-weight: bold;
  margin-bottom: 2px;
}

.message-time {
  text-align: right;
  font-size: 0.75rem;
  margin-top: 2px;
}
</style>