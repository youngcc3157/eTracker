
class Email:
	def __init__(self, message_id, thread_id, label_id, history_id, subject, 
					sender_email, body):
	    self.message_id = message_id
	    self.thread_id = thread_id
	    self.label_id = label_id
	    self.history_id = history_id
	    self.subject = subject
	    self.sender_email = sender_email
	    self.body = body

	def __str__(self):
		return self.subject