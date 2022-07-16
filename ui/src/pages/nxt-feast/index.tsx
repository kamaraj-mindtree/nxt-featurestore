import React, { useContext } from "react";

import {
  EuiPageHeader,
  EuiPageContent,
  EuiPageContentBody,
  EuiLoadingSpinner,
} from "@elastic/eui";

import { useDocumentTitle } from "../../hooks/useDocumentTitle";
import { NxtFeastIcon16 } from "../../graphics/NxtFeastIcon";
import './index.css';
// import RegistryPathContext from "../../contexts/RegistryPathContext";

const NxtRegistryIndex = () => { 
    useDocumentTitle(`NxT | Feature_store_Registry`);
    // const registryUrl = useContext(RegistryPathContext);
    // console.log(registryUrl);
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
        assertIsFormFieldElement(pathField);
        assertIsFormFieldElement(entityField);
        assertIsFormFieldElement(featureViewField);
        console.log(pathField.value,entityField.value,featureViewField.value);
        return fetch('http://127.0.0.1:8889/nxt-feature-store-apply?path='+pathField.value+'&entity_name='+entityField.value+'&feature_view_name='+featureViewField.value, {
        // return fetch('/nxt-feature-store-apply?path='+pathField.value+'&entity_name='+entityField.value+'&feature_view_name='+featureViewField.value, {
            headers: {
              "Content-Type": "application/json",
            },
          })
            .then((res) => {
              return res.json();
            })
    };
    return (
        <React.Fragment>
          <EuiPageHeader
            restrictWidth
            iconType={NxtFeastIcon16}
            pageTitle="NxT Features Registry">
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
                        {/* <span>
                            <input type="submit" />
                        </span> */}
                        <button id="nxt-feast-submit"> Submit </button>
                    </form>
                </div>
            </EuiPageContentBody>
          </EuiPageContent>
        </React.Fragment>
    );
    
};

const NxtMaterializeIndex = () => { 
    useDocumentTitle(`NxT | Feature_store_Materialize`);
    const now = new Date();
    now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
    var max =  now.toISOString().slice(0, -1);

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
        // return fetch('http://127.0.0.1:8889/nxt-feature-store-apply?path='+pathField.value+'&entity_name='+entityField.value+'&feature_view_name='+featureViewField.value, {
        // // return fetch('/nxt-feature-store-apply?path='+pathField.value+'&entity_name='+entityField.value+'&feature_view_name='+featureViewField.value, {
        //     headers: {
        //       "Content-Type": "application/json",
        //     },
        //   })
        //     .then((res) => {
        //       return res.json();
        //     })
    };

    return (
        <React.Fragment>
          <EuiPageHeader
            restrictWidth
            iconType={NxtFeastIcon16}
            pageTitle="NxT Feature Materialize">
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

export {NxtRegistryIndex, NxtMaterializeIndex};