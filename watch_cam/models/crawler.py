from icrawler.builtin import BingImageCrawler

class Get_Images:
  getting_input = '[Input Required]'
  search = ''
  custom_filters = None
  total = 500

  def __init__(this,mode,search='',custom_filter = (),total = 500):
    this.mode = mode
    print(f'> Starting Crawler In Mode: {mode} ...')
    if this.mode == 'manual':
      this.get_search()
      this.get_total()
      this.download()
    else:
      this.search = search
      this.custom_filters = custom_filter
      this.total = total
      this.download()

  def get_search(this):
    this.search = str(input(f'{this.getting_input} What are you trying to train a new ML model for? '))

  def get_total(this):
    change_default = int(input(f'{this.getting_input} How Many Images Do you want? '))
    if(not change_default):
      print('Moving On')
    else:
      this.total = change_default

  def download(this):
    print('Starting Download...')
    print(this.search)
    bing_crawler = BingImageCrawler(feeder_threads=1,parser_threads=3,downloader_threads=3,storage={'root_dir': f'photos/{this.search.strip()}/'})
    bing_crawler.crawl(keyword=this.search, filters=this.custom_filters, offset=0, max_num=this.total)




start = Get_Images(mode='manual')