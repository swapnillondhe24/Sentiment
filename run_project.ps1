# Open the first Anaconda PowerShell prompt

Start-Process "anaconda-prompt.exe" -ArgumentList "/K cd D:\Sentiment\Sentiment-final\Sentiment & python -m Backend.app" -WindowStyle Hidden

# Wait for a few seconds
Start-Sleep -Seconds 5

# Open the second Anaconda PowerShell prompt
Start-Process "anaconda-prompt.exe" -ArgumentList "/K cd D:\Sentiment\Sentiment-final\Sentiment\frontend\fake-review-detection & npm start" -WindowStyle Hidden
