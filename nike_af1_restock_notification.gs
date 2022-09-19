const URL =
  'https://www.nike.com/jp/t/%E3%83%8A%E3%82%A4%E3%82%AD-%E3%82%A8%E3%82%A2-%E3%83%95%E3%82%A9%E3%83%BC%E3%82%B9-1-07-%E3%83%95%E3%83%AC%E3%83%83%E3%82%B7%E3%83%A5-%E3%83%A1%E3%83%B3%E3%82%BA%E3%82%B7%E3%83%A5%E3%83%BC%E3%82%BA-KLdm7l/DM0211-100';
const MY_SIZE = 'JP 26';
const PRODUCT_NAME = 'NIKE AF1';

const replaceBoolWithCheckBox = () => {
  const activeSpreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = activeSpreadsheet.getSheetByName(PRODUCT_NAME);
  const row = sheet.getLastRow();
  const column = 3;
  const numRows = 1;
  const numColumns = 18;
  const lastRowBoolValuesRange = sheet.getRange(
    row,
    column,
    numRows,
    numColumns
  );
  const validateCheckBox = SpreadsheetApp.newDataValidation();
  validateCheckBox.requireCheckbox();
  validateCheckBox.setAllowInvalid(false);
  validateCheckBox.build();
  lastRowBoolValuesRange.setDataValidation(validateCheckBox);
};

const generateSizeList = () => {
  const unavailableSize = 31.5;
  const minSize = 23;
  const maxSize = 32;
  const step = 0.5;
  const len = Math.floor((maxSize - minSize) / step) + 1;
  return Array(len)
    .fill()
    .map((_, idx) => {
      const size = minSize + idx * step;
      if (size === unavailableSize) return undefined;
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
  const activeSpreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = activeSpreadsheet.getSheetByName(PRODUCT_NAME);
  sheet.appendRow([date, time, ...result, JSON.stringify(log)]);
};

const sendLINE = () => {
  const lineNotifyUrl = 'https://notify-api.line.me/api/notify';
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
  UrlFetchApp.fetch(lineNotifyUrl, options);
};

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
  const stockAvailabilityList = [];
  const html = phantomJSCloudScraping(URL);
  const rawShoesDataList = Parser.data(html)
    .from('name="skuAndSize"')
    .to('</div>')
    .iterate();
  const sizeList = generateSizeList();
  sizeList.forEach(size => {
    let isFoundShoesAvailable = false;
    const foundRawShoesData = rawShoesDataList.find(rawShoesData =>
      rawShoesData.includes(size)
    );
    if (foundRawShoesData) {
      isFoundShoesAvailable = foundRawShoesData.indexOf('disabled=""') === -1;
      if (isFoundShoesAvailable && MY_SIZE === size) sendLINE();
    }
    stockAvailabilityList.push(isFoundShoesAvailable);
  });
  saveLog(rawShoesDataList, stockAvailabilityList);
  deleteTrigger();
};
