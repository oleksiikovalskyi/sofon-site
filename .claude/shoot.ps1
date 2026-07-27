# Headless screenshots of local pages -> PNG, so Claude can review layout visually.
# Usage:  powershell -File .claude\shoot.ps1 [-Width 1440] [-Height 1600] [-Only osnastka]
#
# ⚠ МІНІМАЛЬНА ШИРИНА — 500px. Windows не дає вікну бути вужчим, тож при
#   -Width 390 сторінка верстається на 500, а PNG виходить 390 — тобто ти
#   дивишся на обрізаний кадр ширшої верстки й бачиш «переповнення», якого
#   насправді немає. Скрипт тепер сам піднімає ширину й попереджає.
#   Для справжніх 360-390px міряй через JS у панелі браузера: вона віддає
#   будь-яку ширину, просто не рендерить картинку.
param(
  [int]$Width = 1440,
  [int]$Height = 1600,
  [string]$Only = "",
  [string]$Url = "",          # разовий знімок довільного шляху, напр. -Url "/home-ab/f.html?gal=bay"
  [string]$Name = "adhoc",    # ім'я PNG для -Url
  [string]$OutDir = "$env:LOCALAPPDATA\Temp\claude\shots",
  [string]$Base = "http://localhost:8123"
)

# Текст повідомлення навмисно чистий ASCII: файл без BOM, PowerShell 5.1 читає
# його як ANSI, і довге тире всередині рядка перетворюється на друкарську лапку,
# яку парсер приймає за кінець рядка. У коментарях це нешкідливо, у рядках - ні.
if ($Width -lt 500) {
  Write-Host "WARNING: width $Width raised to 500 (Windows minimum window width). A narrower shot would be a cropped frame of a 500px-wide layout." -ForegroundColor Yellow
  $Width = 500
}

$chrome = "C:\Program Files\Google\Chrome\Application\chrome.exe"
if (-not (Test-Path $chrome)) { $chrome = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" }
if (-not (Test-Path $chrome)) { throw "No Chrome/Edge found" }

$pages = @(
  @{ n = "lab";           u = "/lab/" },
  @{ n = "home-a";        u = "/home-ab/a.html" },
  @{ n = "home-b";        u = "/home-ab/b.html" },
  @{ n = "home-c";        u = "/home-ab/c.html" },
  @{ n = "home-d";        u = "/home-ab/d.html" },
  @{ n = "c-tuning";      u = "/home-ab/c-tuning.html" },
  @{ n = "home-e";        u = "/home-ab/e.html" },
  @{ n = "home-f";        u = "/home-ab/f.html" },
  @{ n = "proto-faint";   u = "/home-ab/c-proto.html?reveal=fade&cue=faint" },
  @{ n = "proto-glow";    u = "/home-ab/c-proto.html?reveal=fade&cue=glow" },
  @{ n = "osnastka-a";    u = "/products/osnastka/ab/a.html" },
  @{ n = "osnastka-b";    u = "/products/osnastka/ab/b.html" },
  @{ n = "contract-a";    u = "/contract-manufacturing/ab/a.html" },
  @{ n = "contract-b";    u = "/contract-manufacturing/ab/b.html" },
  @{ n = "custom-a";      u = "/products/custom-equipment/ab/a.html" },
  @{ n = "custom-b";      u = "/products/custom-equipment/ab/b.html" },
  @{ n = "custom-c";      u = "/products/custom-equipment/ab/c.html" }
)
if ($Url) { $pages = @(@{ n = $Name; u = $Url }) }
elseif ($Only) { $pages = $pages | Where-Object { $_.n -like "*$Only*" } }

New-Item -ItemType Directory -Force $OutDir | Out-Null
# унікальний профіль на кожен запуск: спільний профіль інколи лишається заблокованим
# попереднім headless-процесом і сторінка знімається порожньою
$profile = Join-Path $OutDir ("p" + [guid]::NewGuid().ToString("N").Substring(0, 8))

foreach ($p in $pages) {
  $out = Join-Path $OutDir ("{0}.png" -f $p.n)
  if (Test-Path $out) { Remove-Item $out -Force }
  $chromeArgs = @(
    "--headless=new", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
    "--user-data-dir=$profile", "--virtual-time-budget=9000",
    "--window-size=$Width,$Height", "--screenshot=$out", ($Base + $p.u)
  )
  $proc = Start-Process -FilePath $chrome -ArgumentList $chromeArgs -NoNewWindow -Wait -PassThru
  if (Test-Path $out) { "{0,-14} OK  {1,8:N0} bytes  {2}" -f $p.n, (Get-Item $out).Length, $out }
  else { "{0,-14} FAILED (exit {1})" -f $p.n, $proc.ExitCode }
}
