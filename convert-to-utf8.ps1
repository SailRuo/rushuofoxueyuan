# Convert all HTML/HTM files to UTF-8 encoding
# This script handles GB2312, GBK, and other Chinese encodings

$ErrorActionPreference = "Continue"
$convertedCount = 0
$errorCount = 0
$skippedCount = 0

# Get all HTML and HTM files recursively
$files = Get-ChildItem -Path "rushuofoxueyuan" -Include *.html,*.htm -Recurse -File

Write-Host "Found $($files.Count) HTML/HTM files to process..." -ForegroundColor Cyan
Write-Host ""

foreach ($file in $files) {
    try {
        Write-Host "Processing: $($file.FullName)" -ForegroundColor Yellow
        
        # Try to read with GB2312 encoding first (most common for Chinese sites)
        try {
            $encoding = [System.Text.Encoding]::GetEncoding("GB2312")
            $content = [System.IO.File]::ReadAllText($file.FullName, $encoding)
        }
        catch {
            # If GB2312 fails, try GBK (superset of GB2312)
            try {
                $encoding = [System.Text.Encoding]::GetEncoding("GBK")
                $content = [System.IO.File]::ReadAllText($file.FullName, $encoding)
            }
            catch {
                # If both fail, try default encoding
                $content = Get-Content -Path $file.FullName -Raw -Encoding Default
            }
        }
        
        # Update charset meta tag if present
        $content = $content -replace 'charset=gb2312', 'charset=utf-8'
        $content = $content -replace 'charset=gbk', 'charset=utf-8'
        $content = $content -replace 'charset=GB2312', 'charset=UTF-8'
        $content = $content -replace 'charset=GBK', 'charset=UTF-8'
        
        # Save with UTF-8 encoding (with BOM for better compatibility)
        $utf8 = New-Object System.Text.UTF8Encoding $true
        [System.IO.File]::WriteAllText($file.FullName, $content, $utf8)
        
        Write-Host "  ✓ Converted successfully" -ForegroundColor Green
        $convertedCount++
    }
    catch {
        Write-Host "  ✗ Error: $($_.Exception.Message)" -ForegroundColor Red
        $errorCount++
    }
    
    Write-Host ""
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Conversion Complete!" -ForegroundColor Green
Write-Host "  Converted: $convertedCount files" -ForegroundColor Green
Write-Host "  Errors: $errorCount files" -ForegroundColor Red
Write-Host "========================================" -ForegroundColor Cyan
