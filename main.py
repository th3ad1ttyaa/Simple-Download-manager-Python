import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import requests
import os
import time
import datetime
import urllib.parse
import threading
import base64
from PIL import Image
from io import BytesIO
import tempfile

class DownloadManager:
    def __init__(self, root):
        self.root = root
        self.root.title("HexaPals Download Manager")
        # Convert base64 icon to Image
        base64_icon = 'iVBORw0KGgoAAAANSUhEUgAAAjoAAAJsCAYAAAD0nwkqAAAACXBIWXMAAC4jAAAuIwF4pT92AAAgAElEQVR4nO3d/VVcR7Y34ONZ8790I5AcgXAEwqsCMBOBcATGEQhFYBSBUARGAZxliMAQgSGC10SgdxXajVqIj/7u+nietfra4+vRnD4N3b/etWvXD58/fx5YXEppZxiG58MwTP6a7d7zB74chuHFMAzXwzCc3/P/z//s3/j70/x/xnE89dIAwOIEnRlFoJl+TILLuk2CUX5c5r8KQAAwG0HnHiml51GV2Ym/vi7uIofhIio/OQCdjuN4WcA1AUBRBJ0QFZu9eLwq4qLmcxXB5ySCz7+r/MMBoEZdB52U0iTY7G5oGWqTcsXnOAcf1R4AetVd0InKzX48nhVwSZsg9ADQpS6CTvTcTMJNjctSq3Q2FXosbwHQtKaDTkop74w6jOWpXqo3s7qOfp5DVR4AWtVk0Ekp7UbAKXG3VIlyledoHMeT3m8EAG1pKugIOEu7igrPceXPAwBuNBF0BJyVE3gAaELVQSd2UB0JOGsj8ABQtSqDTuyiygHnTQGX04OzCDyOngCgKtUFnZTSQSxT2UW1eR+HYTiwLR2AWlQTdCxTFeM6qjtHvd8IAMpXRdBJKeUKztsCLoWvzqK6c+6eAFCqooNOVHGOTTMu2u+qOwCUqtigoxenKrm6s2/CMgClKS7oxI6qXMX5pYDLYXbXEXZMVwagGP8p6WJiqepcyKlSrrz9mVKyjAVAMYqp6KSU9mNXlaWq+uWlrD3b0AHYtiIqOlEF+CDkNCOPADiPCh0AbM1WKzr6cZp3HZUdE5UB2IqtBZ0IOae2jnfhV+dlAbANW1m6iiUNIacfH6IHCwA2auMVnamQox+nPx/HcRR4ANiYjVZ0hJzuvUkpWcICYGM2FnSEHIKwA8DGbCToCDnc8SYOagWAtVp7j46QwyPsxgJgrdYadGILeT7S4YWXkQcIOwCszdqCjjk5zOGncRzP3TAAVm2dPTrHQg4zOk0pvXSzAFi1tQSd2FXjWAdmlfu3TqIKCAArs/KgExNw33iJmNOrOL0eAFZmpT06scPqby8PS/h9HEeBB4CVWFnQscOKFdKcDMBKrHLp6ljIYUX06wCwEisJOimlA83HrNAL/ToArMLSS1f6clij/43jeOIGA7CoVVR0TLVlXY4tYQGwjKWCThzMaCgg6/LMEhYAy1h46cqSFRv08ziOp244APNapqLjmzabYnkUgIUsFHRi+vFrt5wNeRHLpAAwl7mXrqI59DL6J2BTrodheDmO47/uOACzWqSicyjksAXP4mcPAGY2V0UnpfRyGIZ/3F626MdxHC+9AADMYt6Kjm/UbJufQQBmNnNFJ6W0OwzDX24tBVDVAWAm81R0fJOmFH4WAZjJTBUd1RwKpKoDwJNmrejsu5UURlUHgCc9WdGx04pCmasDwJP+O8O/45vzbPIH7/kwDKfx1/wBfPnQ8kqcFZaHL76Mx048XhT43EqU5+oc+PkE4DGPVnRMQX7SRZzDdDqO4/kq/sC457tTD6fDP+xqHMeXpV4cANv3VNDJ35j/8Dp94zoOND3eRDNsLB3uRZ+U0PO9/43jeFLaRQFQhqeCzqWllFtXeZlkHMetnaQdoecwgo8q2xefxnHcK+FCACjPg0Enekj+9prdVnCOSml8jeWtg3gIPMPwf5qSAbjPY9vLD9yx4Sw3CI/jeFjSB2m+lnxN0cT8voBL2jbjDwC412MVnX87rxa8izBRvKi+HXfcw3MxjuNOAdcBQGHuDToppdzz8GenL1Zeqtobx/G0gGuZS0opB7O3FV3yKpmUDMB3Hlq66rW5Mzcc79YYcoYvS1o56PwcYa03GpIB+I6g89VF9OOsZB7OtkRI243n0xN9OgB857ugE8tWvfXmXEQlp4mdOxHWegs7r2L7PQDcuq+i01s1Jy/z7Le2PTmeT29hZ7eAawCgIPcFnd4+LHZrX656SISdvY56dvTpAPCNb4JObFPuaRLyr62GnInYidRLeFXRAeAbdys6PX1QfNrmcQ6bFGHu9w6e6rMI6wBwo9egc9XbLp1xHI9i0nPrVHUAuNVr0Gmu+XhG+x306wg6ANy6DTpR8u9hW/mnWgcCLiv6dY7qfhZPEnQAuDVd0emht+HaYaU3QeeqgOtYl2fm6QAwMR10evgmfNT7eUixZKeqA0AXpoNO69+Crzv4gJ/VceO9OnZeAXBjOui8bvyWHHXagPyduA8tb60XdAC4cRN0Opg9oprzPUEHgOZNKjqtL1sdq+Z8K4YIttqUnBuSnxdwHQBs2STotP4NWDXnficlXtSKqOoA0EVF56z3nVaPaHmekKADQBdBp4vzrBbUctCxdAVAF0Gn5eWZpUTf0kXFT+ExKjoA3AadF43eik+akJ/U6rKeig4A3x3q2Zouz7Sa03lVVzs7FR0Ahv+klFoely/oPK3Vik4PB9QC8ISWKzrXMSuGxzW7I80sHQBaDjpCDpavADr3n4Z3XFm2mo0ZQwA0q+Wg4wN8BoYpAtCylpeufIDT+hluADxB0KFlgg5A55oNOpZk5nJW0bUCwMxaHxgIAHRM0AEAmiXoAADNEnQYNG4D0Kr/tDpYL6Vkx83sBB0AmtRyRUfQAYDOCToAQLNy0Pm30SfnQEecXg7Quf+M49jqKd+CDn4GADrX8tLV6wKuAQDYoknQuWjxRUgp7RVwGTWw6wqAJk2CTqt9OoLObAQdAJo0CTqt9unspZQ0pAJApyZBp9Vv9M9UdQCgX61XdLLDAq4BANiCHoLOi5TSfgHXAQBs2E3QGccxNyNfN3zzVXUAoEPTc3Rar+oIOwDQmemg0+Qp5lMOnGgOAH3pKejkHVgnBVwHALAhvSxdTbxKKR2XcSlsgGNAADp3G3SiIbnJoyDueGMXFgD04e6hnq0vX018EHYAoH13g05PPSzCDgA07pugM47jaePzdO4SdgCgYXcrOkNHy1cTH8zYAYA23Rd0etyC/TaldOKkcwBoi6Dz1S95i31KaaeUCwIAlvNd0Ilt5p86va8vhmH421IWALThvorOYILwzVLWqSMjAKBujwWdnnZf3ed1LGXtlXdpAMAs7g06sXzVe1VniPOx/tSoDAB1eqiikx15TW/lRuXLhqs7GrABaNKDQWccx/NOzr6aVcvVHdUqAJr0WEVnUNW5V+vVnaaklHZ7vwcAPXsq6GhKvp/eHQCowKNBJ5qSVXUeproDAAV7qqIzRNBR1XnYpLpj7g4AFObJoGOr+cwmc3dMVQaAQsxS0cl8eM/mWUxVPtcECwDbN1PQGcfxchiG916vmb0ahuGvlNKxZmUA2J5ZKzpDVHX06sznTTQr79d00QDQipmDjh1YC8vLWR+iWdkEYgDYoHkqOkMEnSsv0EJys/LfKaUjy1kAsBlzBZ2o6mhMXs5vlrMAYDPmrejksHM8DMOZ12cpk+Usu7MAYI3mDjrhwIuyEqXsztI7BECTFgo6cbL5Oz8SKzPZnbWtZUE9QwA0adGKzqAxeeUmwwYvLWcBwGosHHSiMVlD7eq9iOUsZ2etwDiOp9U/CQAWtkxFZ/IhYmLyeuTt6P/Yjg4Ai1sq6Axfwk5uTL7wGqyN7egAsKClg07YdzzEWtmODgALWEnQiV1Ytpyv32Q7+on+HQB42qoqOpNBgh/d8434Jfp3DvXvAMDDVhZ0gn6dzXo7DMO5/h0AuN9Kg05sOd/Tr7NRL6ZOR9e/AwBTVl3RyWHnchgGH7ib97qQ4yQAoBgrDzrD1+bkX73MW7Ht4yRKYhkVoHNrCTrD1+Zk52Fth+Mkvvi3hIsAYHvWFnSGL2Hn0E6srXKcBABdW2vQGb6EnX1hZ+te244OQI/WHnSGr2HnzE/Y1tmODkBXNhJ0wp7m0CJMb0ffafy5XhZwDQBs0caCTszY2RV2ipGXs/7Op6MPw9DqcpagA9C5TVZ0psOOZaxy/BZnaAFAczYadIYIO+M47mpQBgDWbeNBZ8JuLDbg3E0G6NvWgs7wNewYKsi6GBgI0LmtBp3h61BBx0UAACu39aAzfD0u4iennrNidl0BdO6Hz58/F3MH4piCE7uAWIVxHH9wIwH6VkRFZ2Icx8vYfq5JGQBYWlFBZ/i6/Tw3Kf9ewOVQL4MpASgv6EyM43gUfTtXZVwRlbHjCoByg87wJezkOSg7lrIAgEUUHXSGb5ey/mdXFgAwj+KDzsQ4jnk3Vt6V9amMK6Jwp14gAKoJOsPX6s6e6g4AMIuqgs7EVHXnfRlXBACUqMqgM3yt7hwMw/CzrcTcY9dNAaDaoDMxjuPpOI47cV6W5SwA4Fb1QWcizsuynAUA3CrqrKtVSSnlCk8eOPi6jWfEAq7HcXzuxgH0rcmgM5FS2ovA86KMK2KTHOoJQDNLV/eJ3Vm5uvOuvKtj3VJKGpIBOtd00Bm+7s46HIbhR8MGu7PT+w0A6F3zQWdiHMfLGDb4s4NCu6GiA9C5pnt0HpNSylWePIfnWblXybL06QD0rZuKzl2xnPXSyehtSynt934PAHrWbdAZvj0Z3XTldgk6AB3rdunqPvHt/8hyVnN+zD1avd8EgB51XdG5y3TlZh32fgMAeqWi84CUUg48x6YrN+OncRzPe78JAL1R0XlAbEfP25P/Zzt6E457vwEAPRJ0nnBnurLT0ev1KkYKANARS1dziOWs/GH5ppqL5q6fx3E8dVcA+iDoLCDOUMq7s15Vd/Hkqtyufh2APgg6S7AdvVo57LzMc5R6vxEArdOjswTb0auVg+llSsmhnwCNU9FZEdvRq2QZC6Bxgs6KRf9ODjwvmnpibfs1qnMANEbQWZOU0kHs0NK/U4dP+VwsfTsAbRF01iil9DyalW1Hr8NVhB3bzwEaIehsQDS9HunfqUau7hw4CBSgfoLOBqWU9iLw6N8p33W8VkeWswDqJehsgf6dquTAcziO41HvNwKgRoLOlkT/Tg47v3V5A+pzFYHH7iyAigg6W2b+TnUEHoCKCDqFcH5WdQQegAoIOoVxflZ1BB6Aggk6BYr+nYN4CDx1OIvAYwYPQEEEnYJF/86hgYNVOYuhg2bwABRA0KmAgYNV+hhDB83gAdgiQaciDgytznUMHDzs/UYAbIugU6FoWD4UeKpxFdWdk95vBMCmCTqV0rBcJf07ABsm6FTOhOUqvY8dWvp3ANZM0GmEHVrVuY7lLPN3ANZI0GlMNCwf2qFVjbMIPOe93wiAdRB0GpVS2osdWvp36mA5C2AN/uOmtil2+LyMeS6UL/dYXcaOOgBWREWnA87Pqo7lLIAVEXQ6EdOVT8zeqYrlLIAlCTodia3o+dDJV73fi4rYnQWwBEGnM8JOtSxnASxA0OlQLGOd6tmp0rs4P8tyFsAMBJ1OxfbzP3u/D5VydhbAjASdjqWUjk1SrpqzswCeIOh0LPp1Li1hVc9yFsADDAzsWHwwHvV+HxrwdhiG81iOBGCKik7n4jDQf3q/Dw2xnAUwRdAhh53c1PqLO9EUy1lA9wZLVwS7d9pjOQvo3qCiw2D5qgeWs4BuCTrcSCldOgeraT+ZqgzblVLafeICzi03r95/W3tCLEzQaddHIQfWI8Z05GnzL+88hvjnc43vSClN/8eLYRj+jcf51F8vVWhnJ+gwkX95Xrsbzbk5FLT3mwCrEMfn3H2scw7Z9JmE32wYiUB0Fu/d51EN8oXmHoIOE8qlbbLzChYUwWYvgs1ugcNVX09/QZ0KP/ksw9NxHPNfu6dHhxsppcPYqUM7rsZxfOn1hNnExozdCDclBpt55YruaeysPen1S4+KDhPWe9tjyQqeEOEmB5v9O0tFLchB7Zd4fEgp5Z6f4wg93bznq+hwI3YD/OVuNONsHMendnhAl6KBeL/RcDOrTxF4juu43MWp6DDhQ7Et+73fALgrBmjumwR/46bSk1I6iirPUatVHkEH2vPe1lP4Yqp6c2CExr3y8tZv+ZFSyo3Mh601MQs60JbcfHjoNaV30XtzGP03tTcVb0rewfVX9PIctbKs5awraMuh7eT0LAeclNJxHGvzRshZyKtoXr5MKVW/DK4ZmRu2lzfBdnK6NVXBeeOnYOVyheeg1iUtS1dMaEaunwZkuiPgbMSrWNKq8oBgQQfacGYKKj0RcLYi9/D8k1J6V9PUdT060IaqqjmxEwYW+dm524PD5uU2h/MZTmMvgqAD9XtXUyk5+sGqeZOkDAJOcV7EctZJ6V9cNCNzI6V06vTyKuXt5C9rKSHHcsP51E6YT7Hmb6cY94oP0cOY9UKZ8vvQXqnL5yo6ULeDykLC8Z3tvnk6a97C6lwuvpEDTlT/LoWc4j2L6s5RiReqosONPC/B1NDqXIzjuFPLRcf4/T8f+VfOIridb/CyKExUcA7iYQZOfS6iulPMcrqgw42Ukh+E+vxcy06r+PA6nzFMvzf4sD8CTlOKWsqydAV1+lTZdvLDOSqGv0Wz8t6ar4kC3FmieivkNGGylFXEkrSKDjdUdKqSvy3t1LLTKqWUl9f+XvC/XuWAMp6mgtONj+M4bnX8hYoO1Oeosg/+ZRoUX0d1x0GlDYnzk85VcLrwJu/q3eYWdBUdbqjoVOMqqjm1bCfP39b/WNEfdxXVHROgKxUBZ55lTNqRm5R3t/HeJehwQ9Cpxq/jOB7XcLHxDe5yDd/Yzd6pjIBD2ErYsXQF9TirJeSEozUtS5i9U4ncUB6jKz4IOcThoKfRt7cxgg49eR/LH7Wqpk8ljndY55j+HKD+SCk5SqJA+TWJaet/CjjckcPORo+NEHToxjiOeRhdPoLg99i5VJOPlfWmbKry9Cq2sR47KHT7pgLOX46U4REvorKzkd9ZQYde3FZyxnHMSyo58LyrJPBcxxbcKsQOqU1/i38Ty1lVneLeirwUIeAwp1ebCjuakbnRQTNyHrD33QC6SmZ55NPJq1i2uufQzm1wlMSGxOt96DRxlrD2BmUVHXpx74de/uWKEFFqheeqlpAT7h7auQ25ovB3rixZzlqPHHDycuEwDP8IOSzp1ZKztp4k6NCLRwfs3Qk87wu6JzUtWe0VtmzxNoYNalZekanjGs4FHFbozTqHglq64kYHS1dzHYBZSEk+byev4kN6zkM7t8HsnSU4roENWcucMBUdejFXv0Y+YiHOZ/kx73ja0j2qaU5M6cPgzN5ZkOMa2KCjdczYUdHhRusVnXEcf1jmv7+FCs/WD8Kb1ZKHdm6Dg0JnEEuRR+bgsGErb05W0aEHF8s+x6kKz0/xQblOVW0nX3cj4RrkPqJ/HBR6P8P+2LKVNyer6HCj8YrOyntdosH1cE3Nt7/HrJ/irfjQzm24iOpO91vRo2p5bA4OhVhZv46KDj1Y+RJFbmyO8PTziis8VxWFnOc1HUvxgFeTrehFXt0G3NkqLuRQiqMI30sTdOjB2nox1hB4aprsu65DO7fhbZybtdHDBrfJVnEKl99bTlZxiYIOPVj7luKpwPO/JQ4OPavlPKsNHNq5Dd1Ud2In1aWdVBTu1Sp+HwUderCx/otxHE/i4NBfFwg8NVVzNnVo5zY0W92JRuMccD4IOFTi7bK/i4IOrEFuopsz8LyvZbvzlg7t3LRJdaeJuTt3Dt20k4raLNW3aNcVNxrfdfV/256IG0sFDwWEvJ38ZQ1Tews5tHPTqp27Ew3jR3pwaMDCu1FVdGheCQFiqsLz+z0Hhx5UdDRBSw3Is3odZ2Z9d/p9yaLydink0IiFD+kVdGjdoo3BaxHfSKZPSr9Yx9ku6xAf9L/UcK1rkMPdn3kbduknoufXKfpwNBrTkmeLLmEJOrSuuOWGOyelV1ElmFoC6V2ujpyW2Kg81YdjojGterPI795//TjQuGKXhGK5qpYlqwMfnrdeRdg5LGG4oz4cOpN/1ueadK+iQ+u6H+2/rPgG9bbuZ7FyuYz+R0rpZJtLWfpw6NDrefvlBB1a54Tq5VmyeljuWbqMXXUbk//39OHQsbnekwQdWifoLCE+wJ1/9LgcND7k/piYGL02UwHng6VEOvZini8XenSYuIjeg9YIOgvSgDy3HAj/SinluTuHqzrOI16HvUfmMEGPDmed0G5gIDdit0Zz39zHcfyhgMuoUpxorfdjcRfxRnwy77DBCDe7EXC8BnC/X2cZz6GiQ8tWcZp4lxo9tHPTcoX0j2hazqHnNJrjc+jJIwZuGuWj2ft5jBvYiYflwnZN3pfO7+y6fB6v/eD1n9lMVR1Bh5bZcbU4S1ar9eru0nBKqYGnxRNywD2J96LTeSagx3ErO1OVPcuW38u9Onv5MOXH/iVBh5YJOguILcst9mvBJnyKcHOyzNEusdx5GX/WQQSf/XgIPV8dxD16kB4dbjTao/PTZHmA2XR6aCcs6yqWUI43cfhrzJE5sMR169H3ehUdWnUt5Cykx0M7YVF5aepo0+fVxVLNSfTSHQo8N6Hvwe3m5ujQqpVs7e1J54d2wjxyQ/HP4zjubPNQ3jzCYBzHHHZ+jUOCe/XmsQnlgg6tenTNlm+ZmQMz+RjLJLurmpO0ChG2XkZ/UK9UdOiOoDMfh3bCw3LA+XEcx/1Sl8Rz4/M4jnsdV3cEHbrycZndDp06jYZK4KvpgFPFlPWo7uxG/1BPXsVMqu8IOrTo0Ks6nyjD5zeJ9zVdN6zBdfweVBVwpkXVqcewc29Vx/ZybjS0vTxXczZ6knRrYifHsaUsOvQudlE1UxHu7CiXq3EcX979hyo6tOQqek1YguoOHZosUR22tuwdX/w+FnApm/DivuUrQYdW5HLznt6c1YjGxhwaf9a7Q8Oq68FZRGdh57uKvqBDC/I69K4Bgas3Vd3p5U2SPnQRcKZF2OnhoOO9u/9Ajw43Ku3RyZWGw20O7OpJDBQ8NjmZiuUP+m7CzV0xL+u0g7PsvjkSQtDhRkppPwZOTXse3+anbTsMXceMnOOSBnb1It4oj01QpjJn8aWo+/eMTs6z+30cx9sBqIIOC4umr8nY7em/3536M3eW/IU6ixN88y/mqeWpMqjuUIm8rH0g4Hwrdlb+VdI1rdinGJ54Q9Bho+IX7CmXvZaWa6K6Q8Esaz8hpZTnjb0t+iKXMI7jD5P/tqADLEV1h4JcxxwcQ0NnkFI6b7hf5+dJJc+uK2Ap4zieOFCQLbuOYX8vhZy5fLdDqSG3qwcqOsDKqO6wBR9jmcpy9wIaXsK67dMRdICV0rvDhpxFo7ENCktKKV02eOTL9TiONxtkBB1gLVR3WBM7qVYsxot8aOpJfZGHQl7q0QHWQu8OK5Z3Uv06juOOkLNasTutxanJN3PgBB1gbeLMrFzZ+V80jMK8Jo3GO7aLr1WL91bQATZDdYcFvZ/spHJg73pFiGztAN+boPPf7V8H0IP4oNrTu8MMPkUfjp1Um5WPTfijoedzc6yRig6wUao7POIsBr3tCTlb0dry1c0wRLuugK1R3SE4sqEQKaWTxkZD/KiiA2yN6k73ruOk6ZdCTjFOGns+LwUdYKvszOrS9JENR73fjMK0tnX/uaUroBgxVTl/o3ztVWmWIxsK19ik5HcqOkAxJjuzYvotbTmLSbX7Qk7xmjpWw/ZyoBjRnHzU4Lk7PTuLCo5pxvU4b6gh+aWgA2xdSull7L6yZNUOO6nq1VJFR9ABtid6cg6GYXjrZWjGdQz7E3Dq1dQUakEH2ArLVM25jtfzyHEN1Wuqh8quK2CjLFM1K/fiaDRuREqplXBwZtcVsDEppcNY/xdy2pNf03/yaxxLklAEFR1g7VJKu1HFsUzVh6vo02ltym43GqroXAk6wNrEMtVRY2fnMDvLWZVqKOg4vRxYj6llKiGnX3k56zx+FqhEVGBbcaGiA6yUZSoecBXVHYMDCxe/w3818nTObC8HVsIyFU/IwfevlNLH6N+xBb1cOy09GUtXwNIsUzGHN3lOS0pp300r1suWnoylK2BhUeLOVZxX7iILOIvqTlOHSNYupXTa0AiIM0EHmFvMSTmKb+ewrHcmKpejpR1Xgg63Ukp5TbapIV+aHtcjpZTPpspLVc9afH5sjWblAjTWiJy914zMxFGD02p/KOAammGZijWbNCt/isCjurMde409n381IwOPystUKaXj+JYn5LBuv2hW3qrWgo5dV7QrluNYQixTXerFYcPysuiH3BQbYwvYgHjPbG3+1amgQ8scLLigvEyVUso7Yf7Qi8MW3R4U6kXYiCaraHp0gFt2U1Got7GUpVl5TeJ3v7mgk39eVHSAG/FBYpmKUk2alY/jQ5nV2muwens96NGhcd4MZ5DX5WNA2AfLVFTAZOX1aHF58GYQpaBDyzQjz+bfBkcL0DbNyisUobHFQ3hzhVrQgd6N45jfDD72fh+o0m2zsuWsxcR9a7XZW0UHuHUwWc+GCr3NH2ox1JL5HDRazRkEHeBWTKE9ckeo2KRZ+cRy1mziPh3UcK2LmOzQE3RomTe7+Ryp6tCAX6K60+wH+AodN7wB4WLyN4IOEy2GAkFnDqo6NCR/eP+Rh15azrpfBMGWNyGcT/5G0GGi1TVa5jCO42GcIg0teGX2zvdiyar1adO3gyUFHeAu4/ZpzWT2juWsL046mJkl6AD3G8fxWFWHBlnO+lLNOY5KV8uuYmzGDUGHlhmCtzjffGnVq153Z8VgwB6OeDmZ/g+CDvCdcRzzG8WZO0PDJruzuhg2GFWsDwVcyiZ8c/CroAM8RK8OrXs2NWyw2bOz8nl2d6scDbuOL2q3BB3gXjFsS1WHHryYOjurqf6dCDmnHR3Ye3r3H/x3O9cBm5FL0jEfhsXkXp2/3buFXcc8j9M4YPDyzh+0G/OedjpoEK3B6+jf+ZR/9qcbWmvUYcgZ7qtc/fD58+ftXApFSSm1+oPw82QMOIuJXRo9NDCuynVMnD2Z52cv+kT2IlwKPWX4GIGnui9LUZnqYRv5Xf939/USdLgh6GxWfKjlD7TT0oNY7Ez5p4BLKV1e5juO7flLmRroJmBu33VMDD+qJfBEv1EvjcfTPo7j+PVGIBYAABZoSURBVF2vlR4d2LC8yyOWMN7W0PAb5fuPBVxKqc4iUO+uIuQMcc/jDfvHYRg+NXnX6jFpWL4sfYdWvraowPYYcoaHGq5VdLihorN+8S3r8J7jNn5d1QfkukSF4bzDMvhj8lDFw028drEMceyoliJs7HWfh5+RmyGB985FUtGhdTvbfn75DSildBnfsu57EzoqfY5HVHUc+PnVu/yztakPuxzW40383Sb+93jUZIfWZQlb0qOKk383/+o8CD/4uyjo0LqtBYgIOKczvAE9q2QS8VH0K/QsLyP9mA8/3Ua/Rhy6+pMjOoowHXgOtvFlJc7uyl9CfivzFm3Ug0HH0hU3Gl66ehcfDhsTyzzHCxxB8WPp21mjv+htAZeyaTlY7Be0DPo8lkF9wJVjstvuaJ2/x1MbGfYtZd66twl5whwdWJEV7JQ5jrkqJTvq7A32Ovoxilq2i2rSQVQMj/VOFeFZBM/fUkoXUyMGVhJ6Ukp7MX7ATrzvPbqErKLDDRWdxa342/X/7o4vL01HW1ff1bClOH7+juPsJspzFUP7cjP/+SxVwfjS9DK++Ow6oPhRZ3nH42P/gqDDjYaDzpO/BIuaKiEfrPAb9YM7B0oSzdWtVnWqnIobAfRIdaca9x2v8tJy1Nye/HKoGRkWEB8qk1k4q/xgeRF9MKVr8cDPyTycvRpH/8cOsB3nk1Xj9T0PIWc+V7NUwAUdmEMOOFNbxdf1zfkgStfFig/VVj5Qr2KW0W7tx4XEoMFcwfzdDjk6MNMXLkEHZhBbxc8fmYWzSs8qqZjUXtXJQeD3vFRY+sDGeUXztOoOLTub9fdW0KF1S1VG7szC2eRBi29i0mmxovpR4wfpdTQavyxtN9Uqqe7QuJm/aNleTusWqr4UcqjiUQmTnZ9wGCGwFtWeRr2oHOZSSicLznaCEp3Ns8ysogNTcsCJQ/H+KWBexauYfFqseLOp4cDPjzGQcb+nkDOhukNj5jp6Q9CBr+fFHMasi5IGchV9WnIouVcnL639FAGnup1Uq6Z3hwa8n/d3WdCha1MBZx1bxVeh+MbkeNMpraoz2Sqed1KdF3A9xVDdoWLXi7wfCjo0L6V0b59LzMI5LzTgTPvtoedQkFLC2MVUwKl6q/i6qe5QoYWWngUdevDN0k8+M2ZqFk4tA7qK3h0UVZ13W7yEySycHQFndqo7VOTTosfjCDp0Y2qr+J8VTiB9HYf6lexoCx+Wk4DT3CycTZqq7nzq51lTkes4amchzrriRsNnXQ3xbXWvga21+UN9p+RdQ9Hv9HYD/1PXsU1cuFmxCNRORKckSx12rKJDD/5oZH7Ii2W+1WzIuqs608P+hJw1iA+Ul6o7FGLhJasJFR1uNF7Rac2PJW+VjibvDyv+Y68jRB31OAdnW2I697HDJtmSlVSxVXSgPqU3Jh/HG9QqTFdwDoWczYrG7ty7876n500x9lbxOy/oQH1+Kf0crBVtN/8Y3+YEnC3K934cx7xk+lNs34dN+H1VM7AsXXHD0lV1rvJOo5IvOk57X+Qg1BxwDk0yLlM0nB9oVmaNPuZp5qv641V0oE4vSj8Ha4HG6enzqIScQuUKm0GDrNHFqjddqOhwQ0WnStfRu1LydvPTGXa8nUUFx6C/ytiKzopdx3L1Sr/oqOhAvZ6V3pj8RK/OmeMa6ja1FV2zMsvKIWd3HdVcFR1upJT+9a2sWj+XHBRSSvnD8Jepf3QRw/6Em4ZEg/zRgn1Z8Ou6ZmOp6DDhhOd6FX26+dR6u/OoGpZf0/zaxjgA52Yxj7WFnEHQgSa8jiF9RYpS9M/Oo+rDVLOyycrMYq0hZ7B0xcSMTaOUq/jGZPoTzcpHJivzgHcRjNdKRQfa8KyCc7DoTDQrT5azYNrHTYScQdCBprxNKRU9RJD+xGTlw5isbPYOQ1RyNrbcLuhAW/TAUKQ8zj+PEsg9GZqVu/brpio5E4IOtOV19EVAkaLx1OydPq298fg+gg4Ttvu2o/QhgnTuzkGhlrPalyt4/9vWrktBB9rzIg5ehKJZzurCZOLxybaerKADbTrQmEwtLGc16yLOrtrqQFpBB9r0rIKJyXDLclZzPq7r7Kp5CTrQrjdx/hBUw3JWE37P28dLGWAq6EDbNCZTJctZVcrn2f00jmNR7zuCDhM77kSTXqWUTEymSpazqvKphH6c+zjrihvOumqac7BoQhxee+jsrKLk95f9be6qeoqKDhN26LRLYzJNiOUsZ2eVY1LFKTbkDCo6DF++JT0fhuH/uRnNyls8D8ZxNBSSZsT4hGOV6K0ovoozTdBhiJ05f7kTzclvRoelNQbCKsX717HlrI15H+8r1SyF/7eAa2D7nI3UnurejGARUal8qX9n7c6iMlxcs/FTVHTI34jyD+4rd6IJZ1FS3vqQLtgGgWflruI9pdqlb0Gncyml3Nj3d+/3oQFX8W2rijVzWDeBZ2lXURXeykGcqyTodC6llH+I3/R+HyqW+3COxnG0qwruEYHnQNV6ZhfxnlJ9wJkQdDoWuxb+6f0+VOxTVHEsU8EToml53xe7B32KgNPc7kxBp2OqOdWyXRwWFF/w9uPR+7LWdexYO2r5C5Og0ylbyqtkuzisUPQoHsTO02cd3dtcvTlpaXnqMYJOh2JA4GVnv9i1+xhVHNvFYQ1SSnsReFoNPTfhJgJOV+8jgk5nIuScasyrhmUq2LCo9ExCT63vldcRbE57DDfTBJ3O6MupxnUEnC5Ky1Cq+HK4G4+dgo+cuI5Qc/OocbDfugg6nYhf1vyh+Uvv96ICphpDwaLic/exyeWuq2g/yKEmB5pzuy8fJuh0IHYZnFiuKl61I9aB200eQ1R/hghCz6duzVPVoOsILhOX8fg3/vm/3h/mJ+g0LhrsjjUeF81UY4A1cahnoyxVVeFmqnHMsLBMBbAGgk6DYuT5kSpO0T5GH451dYA1EnQaEstUR6Z9Fu0sAo7t4gAbIOg0IBrgDgve9khDJwED1ETQqZiAUwV9OABbJOhUSMCphmMbALZM0KlIDKk6EnCK9ykCjkZjgC0TdCoQA/8OHd1QPI3GAIURdAom4FQjNxrvCzgA5RF0ChTD/g6GYXjb+70onJ1UAIUTdAoyFXAODPsrmoADUAlBpxAxzfjQsL+iCTgAlRF0tsw04yoIOACVEnS2xCycKuRdVMcCDkC9BJ0Ni51UR04VL9pFzMGxiwqgcoLOhkSjca7g/NbFE67TdQQcFRyARgg6G5BSOrSTqnifYhaO4xoAGiLorJGdVFW4joBz0vuNAGiRoLMGGo2rcREh57z3GwHQKkFnhTQaVyWHnF1LVQBtE3RWwJEN1RFyADoh6Cwp+nCONBpXQ8gB6Iigs6Dow8kB51WVT6BP13ZWAfRF0JmTPpyqHWo8BujLD58/f/aSz0AfTvXOxnHc7f0mAPRGRWcG5uE04aD3GwDQI0HnESmlnVimMg+nbh8tWQH0SdC5RyxT5YDzpriLYxHOrgLolB6dO1JKB7FMZbt4G67GcXzZ+00A6JWKTojt4sf6cJrjDCuAjnUfdGwXb56gA9CxrpeuUkqHsRvHMlWjxnH8ofd7ANCzLis6lqm6cdb7DQDoXVdBxzJVd2wpB+jcf3p5+rFMdS7kdMWZVgCda76iY5mqa6e93wCA3jUbdCxTAQBNLl1ZpgIAhtYqOpapuEMzMkDnmpij42wq7mOGDgDVL13F2VSXQg4AcFe1S1cppZ1YpnpVwOUAAAWqbukqlqlys/FvBVwOZftpHEd9OgAdq6qio9mYOT13wwD6VkXQUcUBABZRfNCJXpwTVRwAYF5F77qKwX9/CzkAwCKKrOjEUlWu4rwu4HIAgEoVF3RiqSofxvisgMsBACpW1NJVSmk/lqqEHFbBriuAzhUTdFJKedv4hwIuhXbseC0B+rb1pSv9OADAumw16ETIOXWMAwCwDltbuoqm43MhpwjX8QCApmwl6EztrDIfZ/s+DsPwMkInADRl40HH9vFinA3D8PM4jvvjOP7b+80AoE0b7dERcoqQl6gOxnE87v1GANC+jVV0hJwivM/LVEIOAL3YSEVHyNm6vEyVl6guO78PAHRm7UFnagu5kLN5V7FMddLbEweAYd1BR8jZmtyHczSO42Gnzx8Abqy7omMY4Obl7eKHlqkAYI1BJ86uEnI25ywCzmkvT3gGu8VfIQBrtZagk1I6GIbhjZduI2wXB4AHrHx7eUopf4v+ww3fiHe2iwPAw1Za0Zk6iZz1+hRVHH04APCIVS9d2WG1XhcRcPThAMAMVhZ0UkqHmo/XRh8OACxgJT060Zfz1guwFvpwAGBBS1d0oi/Hh/DqObYBAJa0iqWrvGT1wguxMlcRcPThAMCSlgo6sWT1mxdhJa5j4N9RA88FAIqwcNCxZLVSH6PZ+N+GnhMAbN0yFZ0DS1ZLO4uAc1758wCAIi0UdFJKL+2yWort4gCwAYtuL/cBvTjbxQFgQ+au6EQD8msv0NxK3y6uPwiA5iyydGVX0HyuYpmq9DPAcp/QLwVcBwCszFxLVymlfcc8zOX9MAw7FYQcAGjSvBWdQz8GM7GbCgAKMHPQiWqO7eSPM/QPAAoyT0VHNedxn6LZWFMvABRipqCjmvMoZ1MBQKFmbUbe9wLea9JsLOQAQIGerOiYm3Ovi2g2FnAAoGCzLF2p5nzr3TiO+pUAoAKPBp04ofyNF/LGRfTi2DIOAJV4qqKjmvOFKg4AVOipoHPQ+YtqR1XdbPUH6NyDu65SSjudbym3o6p+lhkBOvdYRafXZavrqOI4nwoAKvdY0Nnr8MXNZ1TtmW4MAG24N+h0umyl4RgAGvNQRaenZavrGP53XMC1AAAr9FDQ2e3kJueQs2s2DgC06btdVymll8MwvOrg9RZyAKBx920v76GaI+QAQAfuCzo97LYScgCgAz1WdH4VcgCgD98EnejPedbwM/9odxUA9ONuRaflas6Vs7sAoC93g85Ow89+38RjAOhLL0Hno8M5AaA/d4PO6wbvwLUlKwDo023QifOtWnRkyQoA+jRd0Xne4B3I1ZyjAq4DANiC6aDT4o6rE9WcrpmXBNC51is6qjl9E3IBOjcddFrr0bkyARkA+tZyReekgGsAALZoOui8auyFEHQAoHP3HerZBAMCAYCboBOHebbkovtXFgC4rei0FnQ0Ic+vtZ8BAGh26eqygGuojaADQHMEHQCgWYIOANCsZnddAQBMgk6L51wBAJ1T0WGitSNABmddATAJOj4QeNbaHXDWGQCToNPaB4Kt0gBAs0tXgg4A0GzQae0k9rVq8AgQALjRatBpsbF2nQQdAJok6NCqM68sAK02Iz+zHDMX9wqAJt0EnXEcW9xebgji7AQdAJrU8sBAQWd2LQad0wKuAYAtmw46rfU07BVwDbXQ0wRAk1qu6OQ+HWFnNq9quMg5mYoMwDdBp8VSv6DzhJRSq0t8jjUB4Jug0+IHg6DztCaDzjiOenQA+CbotFjqz8tX+wVcR8laDIPXBVwDAAWYDjqXjb4ggs4DYtaQ/hwAmnUbdMZxvGz0m/DrhvtQltXq0p5lKwBu3N111eo34YMCrqFErVa7Wq1OAjCnXoLOL46E+FZUuVpcthosXQEwcTfotFzyPy7gGkrSapXrehxHQQeAG71UdAa9Ol+llPIk5F9KuZ4VE3IAuPVN0ImG5KuGb89RAddQgpbvg0ZkAG7ddwREyx8Ur1JKXTcmx7EYrwu4lHURdAC41VvQyQ57bUxOKT1vvaplIjIA03oMOs86bkzOz/tFAdexLq2dwA/Akr4LOh306QzRmHxYwHVsTByF0WoD8sRJGZcBQCnuq+gMnXxgvO1lF1bssvpQwKWsm2UrAL7Rc9DJTiIENCueXw8B4Mr8HADuujfoRENnDydA3/TrRJNuc6ZCzrMWn98dlq0A+M5DFZ2how+OfAzCaWthp7OQM5h8DcB9BJ0vmgo70XvUU8ixbAXAvR4MOuM4nnSyfDUxCTtVz9iJ3WR/dRRyBstWADzksYrO0OFyQA475zU2KOeAllLKVZy3BVzOplm2AuBegs73ciXk75qOiohrPW/8aIeHXFi2AuAhP3z+/PnRm5NSOo9KR4/ypN39GKJYnOjFaX3a8VN+HcdRRQeAez1V0Rk6P/E7V0j+yX0vJTUq54M5Y5nqr85DzrX+HAAeM0tFJ3/AX3bW3Hqf6wh9R+M4/rvp//F4HfIxDgedh5tpH8dx3C/ncgAozZNBZ/jyIZs/4H/z6t2YVBGO1t0bEuFmLx6tn1O1iB9LXVYEoAyzBp285fofr9l3riL0nMQ06aVEsNmdevTaGzWLs3EcuzirDIDFzRR0hi8fwrnh8417/aizWOa7jF1Q00tc+Z/dndGTP6hzuNmJR+/Lg/P4eRXhEoC2zRN08gfx334eKIBqDgAzmWXX1Y3oRzlzWynAoRcBgFnMHHSCDxi27cySFQCzmivoxAfMR3eXLRK2AZjZvBWdwQcNW6SaA8Bc5g46MbdEVYdtELIBmMsiFZ0hpvNeu9Vs0EfVHADmtVDQiSMQfLtmU679vAGwiEUrOjns5GMhLtx1NuDIUQ8ALGLhoBMO3HXW7GIcR9UcABayVNCJnon3bj1rJEwDsLBlKzpD9E5ceQlYg/cakAFYxtJBJxqT970KrNiVBmQAlrWKis5kCeudV4MV2o8QDQALm/n08lmklPLBn6+8HCzpnQZkAFZhJRWdKXsGCbIku6wAWJmVBp2YdaJfh0VdR1gGgJVYdUUnh50T/TosaM9gQABWaeVBZ/gSdvLSwyevFHP43VZyAFZtLUEn7Dsighl9jCNFAGCl1hZ0YmvwruZknnBh+jEA67LOio6ww1NyyNk1LweAdVlr0Bm+hJ1zYYd7XBsKCMC6rT3oDMIO37uOSs65ewPAOm0k6AzCDl8JOQBszMaCziDsIOQAsGEbDTqDsNMzIQeAjdt40BmEnR4JOQBsxVaCzvBt2DFUsG1CDgBb88Pnz5+3evdTSs+HYcij/1/5MWjOhfOrANimrQediZTS8TAMb4q4GFbhLEKOOTkAbE0xQWf4Enby+VgfCrgUlpPPrtp3DwHYtqKCzvAl7OwMw3AyDMOLAi6H+f06juOx+wZACbbWjPyQaFrNYeeTn5CqXA3D8JOQA0BJiqvoTEsp5VOtD4dheFbOVXGPT86tAqBERQed4UvYeTkMQ64SvC7gcvhW3jp+OI7jkfsCQImKDzoTqjvFOYsqjq3jABSrmqAzfK3u5OrBLwVcTq9UcQCoRlVBZyKltBvLWXZmbVbuxTlQxQGgFlUGnYmYu3NkOWvtLiLgnDb+PAFoTNVBZ/h6hMRBPASe1bqKZSpbxgGoUvVBZ0LgWanrqJQd2TIOQM2aCToTU4FnXw/P3AQcAJrSXNCZFj08+2bwPMkSFQBNajroTMT5WbnKs2dZ6xsf8+41TcYAtKqLoDMtqjx7Hc/iuYit+ceWpwBoXXdBZyJ6efY6CT1XcSL8cRyaCgBd6Dbo3JVSyoFnN4JPC03MebhfXpI6MeAPgF4JOveIoyZy6NmJv74q7iK/lXdLnUewOdVzAwBfCDozimMncvB5GX/d2VJjc+6x+TdCTQ435yo2AHA/QWdJEYCGqPwMEYReTv2ps25tnwSYiUlV5nLyEGgAYA7DMPx/F/maIp/cCuUAAAAASUVORK5CYII='  # Replace with your actual base64 icon
        icon_data = base64.b64decode(base64_icon)
        icon_image = Image.open(BytesIO(icon_data))

        # Save the image to a temporary file
        temp_icon_file = tempfile.NamedTemporaryFile(delete=False, suffix=".ico")
        icon_image.save(temp_icon_file.name, format="ICO")

        # Set the taskbar icon using the temporary file
        self.root.iconbitmap(temp_icon_file.name)

        self.url_label = tk.Label(root, text="URL:")
        self.url_label.pack()

        self.url_entry = tk.Entry(root, width=50)
        self.url_entry.pack()

        self.check_button = tk.Button(root, text="Check URL", command=self.check_url)
        self.check_button.pack()

        self.file_info_label = tk.Label(root, text="")
        self.file_info_label.pack()

        self.progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
        self.progress.pack()

        self.download_button = tk.Button(root, text="Download", state="disabled", command=self.start_download)
        self.download_button.pack()

        self.file_name_label = tk.Label(root, text="")
        self.file_name_label.pack()

        self.download_size_label = tk.Label(root, text="")
        self.download_size_label.pack()

        self.download_speed_label = tk.Label(root, text="")
        self.download_speed_label.pack()

        self.estimated_time_label = tk.Label(root, text="")
        self.estimated_time_label.pack()

        self.downloading_thread = None

    def check_url(self):
        url = self.url_entry.get()
        try:
            response = requests.head(url)
            if response.status_code == 200:
                file_size = int(response.headers.get("Content-Length", 0))
                self.file_info_label.config(text=f"File Size: {file_size / (1024 * 1024):.2f} MB")
                self.download_button.config(state="active")
                self.file_name_label.config(text=f"File Name: {os.path.basename(urllib.parse.urlsplit(url).path)}")
            else:
                self.file_info_label.config(text="Invalid URL")
                self.download_button.config(state="disabled")
                self.file_name_label.config(text="")
                self.download_size_label.config(text="")
                self.download_speed_label.config(text="")
                self.estimated_time_label.config(text="")
        except requests.exceptions.RequestException:
            self.file_info_label.config(text="Error checking URL")
            self.download_button.config(state="disabled")
            self.file_name_label.config(text="")
            self.download_size_label.config(text="")
            self.download_speed_label.config(text="")
            self.estimated_time_label.config(text="")

    def start_download(self):
        if self.downloading_thread is None or not self.downloading_thread.is_alive():
            self.downloading_thread = threading.Thread(target=self.download_thread)
            self.downloading_thread.start()

    def download_thread(self):
        url = self.url_entry.get()
        file_size = int(requests.head(url).headers.get("Content-Length", 0))
        file_extension = os.path.splitext(urllib.parse.urlsplit(url).path)[1]
        save_path = f"downloaded_file{file_extension}"
        downloaded = 0
        start_time = time.time()

        response = requests.get(url, stream=True)
        with open(save_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    self.update_gui(downloaded, file_size, start_time)

        self.update_gui(downloaded, file_size, start_time, completed=True)
        messagebox.showinfo("Download Complete", "File downloaded successfully!")

    def update_gui(self, downloaded, file_size, start_time, completed=False):
        elapsed_time = time.time() - start_time
        remaining_bytes = file_size - downloaded
        download_speed = downloaded / elapsed_time if elapsed_time > 0 else 0
        estimated_remaining_time = remaining_bytes / download_speed if download_speed > 0 else 0

        self.root.after(100, self.update_labels, downloaded, file_size, download_speed, estimated_remaining_time, completed)

    def update_labels(self, downloaded, file_size, download_speed, estimated_remaining_time, completed=False):
        self.progress["value"] = (downloaded / file_size) * 100

        self.download_size_label.config(text=f"Downloaded: {downloaded / (1024 * 1024):.2f} MB")
        self.download_speed_label.config(text=f"Download Speed: {download_speed / (1024 * 1024):.2f} MB/s")

        if download_speed > 0:
            estimated_time = self.format_time(estimated_remaining_time)
            self.estimated_time_label.config(text=f"Estimated Time: {estimated_time}")

        if completed:
            self.download_button.config(state="active")

    def format_time(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours)} hours {int(minutes)} minutes"

if __name__ == "__main__":
    root = tk.Tk()
    app = DownloadManager(root)
    root.mainloop()
