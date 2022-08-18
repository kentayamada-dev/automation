const phantomJSCloudScraping = URL => {
  let source = '';
  const key =
    PropertiesService.getScriptProperties().getProperty('PHANTOMJSCLOUD_ID');
  const option = {
    url: URL,
    renderType: 'HTML',
    outputAsJson: true,
  };
  const payload = encodeURIComponent(JSON.stringify(option));
  const apiUrl =
    'https://phantomjscloud.com/api/browser/v2/' + key + '/?request=' + payload;
  try {
    const response = UrlFetchApp.fetch(apiUrl);
    const json = JSON.parse(response.getContentText());
    source = json['content']['data'];
  } catch (error) {
    console.log(error);
  }
  return source;
};

const main = () => {
  const html = phantomJSCloudScraping("https://www.sacnilk.com/articles/internet/instagram/List_of_MostFollowed_Instagram_Handle_in_World?hl=en");
  const rawShoesDataList = Parser.data(html)
    .from('<a href="https://www.instagram.com/')
    .to('</a>')
    .iterate();
  console.log(rawShoesDataList)
};