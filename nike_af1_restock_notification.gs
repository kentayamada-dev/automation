const URL =
  'https://www.nike.com/jp/t/%E3%83%8A%E3%82%A4%E3%82%AD-%E3%82%A8%E3%82%A2-%E3%83%95%E3%82%A9%E3%83%BC%E3%82%B9-1-07-%E3%83%95%E3%83%AC%E3%83%83%E3%82%B7%E3%83%A5-%E3%83%A1%E3%83%B3%E3%82%BA%E3%82%B7%E3%83%A5%E3%83%BC%E3%82%BA-KLdm7l/DM0211-100';
const MY_SIZE = 'JP 26';
const PRODUCT_NAME = 'NIKE AF1';

const generateSizeList = () => {
  const minSize = 23;
  const maxSize = 32;
  const step = 0.5;
  const len = Math.floor((maxSize - minSize) / step) + 1;
  return Array(len)
    .fill()
    .map((_, idx) => {
      const size = minSize + idx * step;
      if (size === 31.5) return undefined;
      return `JP ${minSize + idx * step}`;
    })
    .filter(e => typeof e !== 'undefined');
};

const setTrigger = () => {
  const today = new Date();
  const hours = today.getHours();
  if (hours > 6 && hours < 24) {
    today.setHours(hours + 1);
    today.setMinutes(0);
    ScriptApp.newTrigger('main').timeBased().at(today).create();
  }
};

const deleteTrigger = () => {
  const triggers = ScriptApp.getProjectTriggers();
  triggers.forEach(trigger => {
    if (trigger.getHandlerFunction() === 'main') {
      ScriptApp.deleteTrigger(trigger);
    }
  });
};

const saveLog = (log, result) => {
  const today = new Date();
  const date = Utilities.formatDate(today, 'JST', 'yyyy/MM/dd');
  const time = Utilities.formatDate(today, 'JST', 'HH:m:ss');
  const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = spreadsheet.getSheetByName(PRODUCT_NAME);
  sheet.appendRow([date, time, ...result, JSON.stringify(log)]);
  const row = sheet.getLastRow();
  const column = 3;
  const numRows = 1;
  const numColumns = result.length;
  const lastRowBoolValues = sheet.getRange(row, column, numRows, numColumns);
  const validateCheckBox = SpreadsheetApp.newDataValidation();
  validateCheckBox.requireCheckbox();
  validateCheckBox.setAllowInvalid(false);
  validateCheckBox.build();
  lastRowBoolValues.setDataValidation(validateCheckBox);
};

const sendLINE = () => {
  const messageText = `${PRODUCT_NAME}[${MY_SIZE}]がリストックされました🎉🎉🎉\n\n${URL}`;
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
  const stockAvailabilityList = [];
  const html = phantomJSCloudScraping(URL);
  const rawShoesDataList = Parser.data(html)
    .from('name="skuAndSize"')
    .to('</div>')
    .iterate();
  const sizeList = generateSizeList();
  sizeList.forEach(size => {
    const mySizeRawShoesData = rawShoesDataList.find(rawShoesData =>
      rawShoesData.includes(size)
    );
    const isMySizeAvailable = mySizeRawShoesData.indexOf('disabled=""') === -1;
    if (isMySizeAvailable && MY_SIZE === size) sendLINE();
    stockAvailabilityList.push(isMySizeAvailable);
  });
  saveLog(rawShoesDataList, stockAvailabilityList);
  deleteTrigger();
};
