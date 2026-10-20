import sys
import logging
from assistant_core.models import Message

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m assistant_core \"<your message>\"")
        sys.exit(1)
        
    user_text = sys.argv[1]
    msg = Message(text=user_text)
    
    # Khởi tạo AssistantService thực tế sẽ được tích hợp sau khi nhóm code xong
    print(f"Message received: {msg.text}")

if __name__ == "__main__":
    main()
