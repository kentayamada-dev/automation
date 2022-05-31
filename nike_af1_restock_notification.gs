const URL =
  'https://www.nike.com/jp/t/%E3%83%8A%E3%82%A4%E3%82%AD-%E3%82%A8%E3%82%A2-%E3%83%95%E3%82%A9%E3%83%BC%E3%82%B9-1-07-%E3%83%95%E3%83%AC%E3%83%83%E3%82%B7%E3%83%A5-%E3%83%A1%E3%83%B3%E3%82%BA%E3%82%B7%E3%83%A5%E3%83%BC%E3%82%BA-KLdm7l/DM0211-100';
const SIZE = 'JP 26';
const REG_WORK_HOURS = /^([7-9]|1\d|2[0-3])$/; //7~23の数字範囲を判定する正規表現
const PRODUCT_NAME = 'NIKE AF1';

function setTrigger() {
  const today = new Date();
  if (REG_WORK_HOURS.test(today.getHours())) {
    today.setHours(today.getHours() + 1);
    today.setMinutes(0);
    ScriptApp.newTrigger('main').timeBased().at(today).create();
  }
}

function delTrigger() {
  const triggers = ScriptApp.getProjectTriggers();
  for (const trigger of triggers) {
    if (trigger.getHandlerFunction() === 'main') {
      ScriptApp.deleteTrigger(trigger);
    }
  }
}

const saveLog = (log, found) => {
  const today = new Date();
  const date = Utilities.formatDate(today, 'JST', 'yyyy/MM/dd');
  const time = Utilities.formatDate(today, 'JST', 'HH:m:ss');
  const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = spreadsheet.getSheetByName(PRODUCT_NAME);
  sheet.appendRow([date, time, '', JSON.stringify(log)]);
  const updatedSheet = sheet.getRange(sheet.getLastRow(), 3).insertCheckboxes();
  if (found) updatedSheet.check();
};

const sendLINE = () => {
  const messageText = `${PRODUCT_NAME}[${SIZE}]がリストックされました🎉🎉🎉\n\n${URL}`;
  const token =
    PropertiesService.getScriptProperties().getProperty('LINE_NOTIFY_TOKEN');
  const options = {
    method: 'post',
    headers: {
      Authorization: 'Bearer ' + token,
    },
    payload: {
      message: messageText,
    },
  };
  const url = 'https://notify-api.line.me/api/notify';
  UrlFetchApp.fetch(url, options);
};

const phantomJSCloudScraping = URL => {
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
  const response = UrlFetchApp.fetch(apiUrl);
  const json = JSON.parse(response.getContentText());
  const source = json['content']['data'];
  return source;
};

const main = () => {
  const html = phantomJSCloudScraping(URL);
  const listOfAvailableSize = Parser.data(html)
    .from('name="skuAndSize"')
    .to('</div>')
    .iterate();
  const mySize = listOfAvailableSize.find(size => size.includes(SIZE));
  const isMySizeAvailable = mySize.indexOf('disabled=""') === -1;
  if (isMySizeAvailable) sendLINE();
  saveLog(listOfAvailableSize, isMySizeAvailable);
  delTrigger();
};
