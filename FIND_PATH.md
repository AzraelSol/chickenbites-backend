# Find Your Backend Directory Path

## Step 1: Find where you are
```bash
pwd
```

## Step 2: List your home directory
```bash
ls -la /home/u761984878/
```

## Step 3: Check if domains folder exists
```bash
ls -la /home/u761984878/domains/
```

## Step 4: Find your actual path
Try these commands to locate your csc4 folder:

```bash
find /home/u761984878 -name "csc4" -type d 2>/dev/null
```

OR

```bash
find /home -name "csc4" -type d 2>/dev/null
```

## Step 5: Check the file manager path
You mentioned your files are at:
`https://srv2049-files.hstgr.io/648de302f61f3d03/files/public_html/csc4/`

This suggests the path might be:
```bash
/home/u761984878/files/public_html/csc4
```

OR

```bash
/home/u761984878/648de302f61f3d03/files/public_html/csc4
```

## Step 6: Navigate and check
```bash
cd /home/u761984878
ls -la
```

Then check what folders exist and navigate to find csc4.

