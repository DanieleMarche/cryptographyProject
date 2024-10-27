import hmac
import hashlib

class WindowController:
    # Other methods ...

    def generate_auth_tag(self, message, key):
        mac = hmac.new(key.encode(), message.encode(), hashlib.sha256).hexdigest()
        print(f"Generated MAC: {mac}, Algorithm: HMAC-SHA256, Key Length: {len(key)*8} bits")
        return mac

    def verify_auth_tag(self, message, key, received_mac):
        mac = hmac.new(key.encode(), message.encode(), hashlib.sha256).hexdigest()
        if hmac.compare_digest(mac, received_mac):
            print("MAC verification successful")
            return True
        else:
            print("MAC verification failed")
            return False





