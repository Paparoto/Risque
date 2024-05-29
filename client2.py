import socket
import threading
import pygame
import sys


class Client:
	def __init__(self, host, port):
		self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.conn.connect((host, port))
		self.messages = []

		self.running = True
		self.input_text = ""

		pygame.init()
		self.screen = pygame.display.set_mode((500, 500))
		pygame.display.set_caption("Chat Client")
		self.font = pygame.font.Font(None, 30)

		self.thread_receive = threading.Thread(target=self.receive_messages)
		self.thread_receive.start()

		self.mainloop()

	def receive_messages(self):
		while self.running:
			try:
				message = self.conn.recv(1024).decode("utf-8")
				if message:
					self.messages.append(message)
			except:
				self.running = False

	def mainloop(self):
		while self.running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False
					pygame.quit()
					sys.exit()
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_RETURN:
						msg = self.input_text.encode("utf-8")
						self.conn.send(msg)
						self.messages.append(msg)
						if msg.lower().startswith(b"attaque"):
							attaque_log = b"attaque vers "+msg[8:]
							self.conn.send(attaque_log)
							self.messages.append(attaque_log)
						self.input_text = ""

					elif event.key == pygame.K_BACKSPACE:
						self.input_text = self.input_text[:-1]
					else:
						self.input_text += event.unicode
			self.screen.fill((0, 0, 0))
			y = 10
			for message in self.messages[-15:]:  # display last 15 messages
				msg_surface = self.font.render(message, True, (255, 255, 255))
				self.screen.blit(msg_surface, (10, y))
				y += 30

			input_surface = self.font.render(self.input_text, True, (0, 255, 0))
			self.screen.blit(input_surface, (10, 450))

			pygame.display.flip()


if __name__ == "__main__":
    host = socket.gethostname()
    port = 50000
    Client(host, port)