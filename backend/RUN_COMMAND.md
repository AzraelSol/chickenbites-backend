# Single Command to Run Backend on Hostinger VPS

## To Run in Background (Keeps Running After You Disconnect):

```bash
cd /home/u761984878/domains/gisrabies.com/public_html/csc4 && nohup python3 start.py > server.log 2>&1 &
```

## To Run in Foreground (See Output, Press Ctrl+C to Stop):

```bash
cd /home/u761984878/domains/gisrabies.com/public_html/csc4 && python3 start.py
```

## Notes:

- Replace the path with your actual backend folder path on Hostinger
- The `nohup` command keeps it running even after you close the terminal
- Logs will be saved to `server.log`
- Server runs on port 8000 by default

## To Check if It's Running:

```bash
ps aux | grep python
```

## To Stop the Server:

```bash
pkill -f "python3 start.py"
```

