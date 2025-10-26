from datetime import datetime
from .models import ActivityLog

def log_activity(user, module, action_description):
   
    try:
        ActivityLog.objects.create(
            user=user,
            module=module,
            action=action_description,
            date=datetime.now().date(),
            time=datetime.now().time()
        )
        print(f"✅ Activity logged: {user.username} | {module} | {action_description}")
    except Exception as e:
        print(f"⚠️ Failed to log activity: {e}")
