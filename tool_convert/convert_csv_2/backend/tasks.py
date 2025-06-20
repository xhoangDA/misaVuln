from celery import shared_task
from .models import ProcessingHistory
import pandas as pd
import tempfile

@shared_task(bind=True)
def process_file(self, history_id):
    history = ProcessingHistory.objects.get(id=history_id)
    history.status = 'PROCESSING'
    history.save()
    
    try:
        # Đọc file input
        input_path = history.input_file.path
        df = pd.read_csv(input_path)
        
        # Xử lý dữ liệu (logic của bạn)
        processed_df = your_processing_logic(df)
        
        # Lưu file output
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as tmp:
            processed_df.to_csv(tmp.name, index=False)
            history.output_file.save('result.csv', tmp)
        
        history.status = 'COMPLETED'
        history.logs = "Xử lý thành công"
    
    except Exception as e:
        history.status = 'FAILED'
        history.logs = str(e)
    
    finally:
        history.save()