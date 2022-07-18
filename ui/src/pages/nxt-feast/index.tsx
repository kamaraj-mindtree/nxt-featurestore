import React, { useContext } from "react";

import {
  EuiPageHeader,
  EuiPageContent,
  EuiPageContentBody,
  EuiLoadingSpinner,
} from "@elastic/eui";

import { useDocumentTitle } from "../../hooks/useDocumentTitle";
import { NxtFeastIcon16 } from "../../graphics/NxtFeastIcon";
import RegistryPathContext from "../../contexts/RegistryPathContext";
import useLoadRegistry from "../../queries/useLoadRegistry";
import DataSourceIndexEmptyState from "../data-sources/DataSourceIndexEmptyState";
import './index.css';

const useLoadFeatureStoreData = () => {
  const registryUrl = useContext(RegistryPathContext);
  const registryQuery = useLoadRegistry(registryUrl);
  // console.log(registryQuery)
  const data =
    registryQuery.data === undefined
      ? undefined
      : registryQuery.data;

  return {
    ...registryQuery,
    data,
  };
};

const NxtRegistryIndex = () => { 
    useDocumentTitle(`NxT | Feature_store_Registry`);
    // const registryUrl = useContext(RegistryPathContext);
    // console.log(registryUrl);
    var response_message = '';
    function assertIsFormFieldElement(element: Element): asserts element is HTMLInputElement | HTMLSelectElement | HTMLButtonElement {
        // Customize this list as necessary −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            if (!("value" in element)) {
                throw new Error(`Element is not a form field element`);
            }
        }
        const handleSubmit = (event: React.FormEvent<HTMLFormElement>) =>{
        event.preventDefault();
        const pathField = event.currentTarget[0];
        const entityField = event.currentTarget[1];
        const featureViewField = event.currentTarget[2];
        const featureServiceField = event.currentTarget[3];
        assertIsFormFieldElement(pathField);
        assertIsFormFieldElement(entityField);
        assertIsFormFieldElement(featureViewField);
        assertIsFormFieldElement(featureServiceField);
        fetch('/nxt/feature-store-apply?parquet_path='+pathField.value+'&entity_column='+entityField.value+'&feature_views_name='+featureViewField.value+'&feature_service_name='+featureServiceField.value, {
            method: 'GET',
            headers: {
              "Content-Type": "application/json; charset=UTF-8",
            },
          })
          .then(res => {
            console.log(res)
            if (res.status>=200 && res.status <300) {
              return res.json()
            }else{
              throw new Error();
            }
        }).then(data=> {
          if (data.status) {
            response_message = data.Message;
            alert(response_message);
            window.location.reload();
          }
        }
          )
         .catch(err=>console.log('fetch() failed'))
    };
    return (
        <React.Fragment>
          <EuiPageHeader
            restrictWidth
            iconType={NxtFeastIcon16}
            pageTitle="Features Registry">
            <div id="nxt-component-1">New</div>
          </EuiPageHeader>
          <EuiPageContent
            hasBorder={false}
            hasShadow={false}
            paddingSize="none"
            color="transparent"
            borderRadius="none"
          >
            <EuiPageContentBody>
                {/* <p>
                  <EuiLoadingSpinner size="m" /> Loading
                </p> */}
                <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>            

                <div id="nxt-feast">
                    <form onSubmit={handleSubmit}>
                        <p>
                            <label><b>Path   :</b></label>
                            <input type="text" placeholder="path to your feature engineered data" required />
                            <br/><br/>
                        </p>
                        <p>
                            <label><b>Entity Name   :</b></label>
                            <input type="text"placeholder="type entity name" required />
                            <br/><br/>
                        </p>
                        <p>
                            <label><b>Feature View   :</b></label>
                            <input type="text" placeholder="type name for featureview" required /><br/><br/>
                        </p>
                        <p>
                            <label><b>Feature Service   :</b></label>
                            <input type="text" placeholder="type name for featureservice" required /><br/><br/>
                        </p>
                        {/* <span>
                            <input type="submit" />
                        </span> */}
                        <button id="nxt-feast-submit"> Submit </button><br/><br/>
                        { response_message != '' ? <div id='myresponse'><span> Deployment is In progress</span></div> :  <div><span></span></div>}
                        
                    </form>
                </div>
            </EuiPageContentBody>
          </EuiPageContent>
        </React.Fragment>
    );
    
};

const NxtHistoricalFeaturesIndex = () => { 

    const { isLoading, isSuccess, isError, data } = useLoadFeatureStoreData();
    // console.log(isLoading, isSuccess, isError, typeof data?.objects.entities?.length);
    useDocumentTitle(`NxT | Retrieve Features`);
    const now = new Date();
    now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
    var max =  now.toISOString().slice(0, -1);
    var response_message = '';

    function assertIsFormFieldElement(element: Element): asserts element is HTMLInputElement | HTMLSelectElement | HTMLButtonElement {
        // Customize this list as necessary −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            if (!("value" in element)) {
                throw new Error(`Element is not a form field element`);
            }
        }
    const handleSubmit = (event: React.FormEvent<HTMLFormElement>) =>{
        event.preventDefault();
        const featureViewName = event.currentTarget[0];
        const entityName = event.currentTarget[1];
        const entityKeys = event.currentTarget[2];
        const startTimeField = event.currentTarget[3];
        const endTimeField = event.currentTarget[4];
        assertIsFormFieldElement(entityKeys);
        assertIsFormFieldElement(entityName);
        assertIsFormFieldElement(startTimeField);
        assertIsFormFieldElement(endTimeField);
        assertIsFormFieldElement(featureViewName);
        console.log(entityKeys.value ,entityName.value, startTimeField.value,endTimeField.value,featureViewName.value);
        return fetch('/nxt/feature-retrieval?feature_view_names='+featureViewName.value+'&entity_name='+entityName.value+'&entity_keys='+entityKeys.value+'&start_date='+startTimeField.value+'&end_date='+endTimeField.value, {
          method: 'POST',
          headers: {
            "Content-Type": "application/json; charset=UTF-8",
          },
        })
        .then(res => {
          console.log(res)
          if (res.status>=200 && res.status <300) {
            return res.json()
          }else{
            throw new Error();
          }
      }).then(data=>{
        if (data.status) {
          response_message = data.Message;
          alert(response_message);
          window.location.reload();
        }
      })
       .catch(err=>console.log('fetch() failed'))
    };

    return (
        <React.Fragment>
          <EuiPageHeader
            restrictWidth
            iconType={NxtFeastIcon16}
            pageTitle="Features Retrieval">
            <div id="nxt-component-1">New</div>
          </EuiPageHeader>
          <EuiPageContent
            hasBorder={false}
            hasShadow={false}
            paddingSize="none"
            color="transparent"
            borderRadius="none"
          >
            <EuiPageContentBody>
                {/* <p>
                  <EuiLoadingSpinner size="m" /> Loading
                </p> */}
                {isLoading && (
                  <p>
                    <EuiLoadingSpinner size="m" /> Loading
                  </p>
                )}
                {isError && <p>We encountered an error while loading.</p>}
                <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
                {isSuccess && !data && <DataSourceIndexEmptyState />}       
                {isSuccess && data &&
                <div id="nxt-feast">
                    <form onSubmit={handleSubmit}>
                        <p>
                            <label><b>Feature View   :</b></label>
                            <select style = {{minWidth: 'fit-content'}} >
                                <option>select</option>
                                {data?.objects.featureViews?.map(
                                    ({ spec }, index) => 
                                <option value={ spec.name } >{ spec.name }</option>
                                )}
                            </select>
                            <br/><br/>
                        </p>
                        <p>
                            <label><b>Entity Name   :</b></label>
                            <select style = {{minWidth: 'fit-content'}} >
                                <option>select</option>
                                {data?.objects.entities?.map(
                                    ({ spec }, index) => 
                                <option value={ spec.name } >{ spec.name }</option>
                                )}
                            </select>
                            <br/><br/>
                        </p>
                        <p>
                            <label><b>Entity Keys   :</b></label>
                            <input type="text" required/>
                            <br/><br/>
                        </p>
                        <p>
                            <label><b>Start Time   :</b></label>
                            <input type="datetime-local" step="1" id="Test_DatetimeLocal_start" max={max} required/>
                            <br/><br/>
                        </p>
                        <p>
                            <label><b>End Time   :</b></label>
                            <input type="datetime-local" step="1" id="Test_DatetimeLocal_end" max={max} required/>
                            <br/><br/>
                        </p>
                        <button id="nxt-feast-submit"> Submit </button>
                    </form>
                </div> }
            </EuiPageContentBody>
          </EuiPageContent>
        </React.Fragment>
    );
};


const NxtMaterializeIndex = () => { 
    useDocumentTitle(`NxT | Feature_store_Materialize`);
    const now = new Date();
    now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
    var max =  (now.toISOString()+1).slice(0, -1);
    var response_message = '';

    function assertIsFormFieldElement(element: Element): asserts element is HTMLInputElement | HTMLSelectElement | HTMLButtonElement {
        // Customize this list as necessary −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            if (!("value" in element)) {
                throw new Error(`Element is not a form field element`);
            }
        }
    const handleSubmit = (event: React.FormEvent<HTMLFormElement>) =>{
        event.preventDefault();
        const startTimeField = event.currentTarget[0];
        const endTimeField = event.currentTarget[1];
        assertIsFormFieldElement(startTimeField);
        assertIsFormFieldElement(endTimeField);
        console.log(startTimeField.value,endTimeField.value);
        return fetch('/nxt/feature-materialize?start_date='+startTimeField.value+'&end_date='+endTimeField.value, {
          method: 'POST',
          headers: {
            "Content-Type": "application/json; charset=UTF-8",
          },
        })
        .then(res => {
          console.log(res)
          if (res.status>=200 && res.status <300) {
            return res.json()
          }else{
            throw new Error();
          }
      }).then(data=>{
        if (data.status) {
          // if(data.detail == 'Not Found')
          // {
          //   response_message = 'Selected Date exceeds than the actual data'
          // }
          // else
          // {
          //   response_message = data.Message;
          // }
          response_message = 'Data Pushed To Online Store'
          alert(response_message);
          window.location.reload();
        }
      })
       .catch(err=>console.log('fetch() failed'))
    };

    return (
        <React.Fragment>
          <EuiPageHeader
            restrictWidth
            iconType={NxtFeastIcon16}
            pageTitle="Feature Materialize">
            <div id="nxt-component-1">New</div>
          </EuiPageHeader>
          <EuiPageContent
            hasBorder={false}
            hasShadow={false}
            paddingSize="none"
            color="transparent"
            borderRadius="none"
          >
            <EuiPageContentBody>
                {/* <p>
                  <EuiLoadingSpinner size="m" /> Loading
                </p> */}
                <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>            

                <div id="nxt-feast">
                    <form onSubmit={handleSubmit}>
                        <p>
                            <label><b>Start Time   :</b></label>
                            <input type="datetime-local" id="Test_DatetimeLocal_start" max={max} required/>
                            <br/><br/>
                        </p>
                        <p>
                            <label><b>End Time   :</b></label>
                            <input type="datetime-local" id="Test_DatetimeLocal_end" max={max} required/>
                            <br/><br/>
                        </p>
                        <button id="nxt-feast-submit"> Submit </button>
                    </form>
                </div>
            </EuiPageContentBody>
          </EuiPageContent>
        </React.Fragment>
    );
};

export {NxtRegistryIndex, NxtHistoricalFeaturesIndex, NxtMaterializeIndex};